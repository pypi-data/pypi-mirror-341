"""
MCP服务端实现 - 处理Git和GitLab操作命令
"""

import os
import subprocess
import logging
from typing import Optional, Dict, Any, List
import typer
from datetime import datetime
import gitlab
import urllib3
from mcp.server.fastmcp import FastMCP
from .connector import GitLabConnector

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gitlab_mcp.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('gitlab_mcp')

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = typer.Typer()
mcp = FastMCP("GitLab-MCP")

# 初始化GitLab连接器
gitlab_connector = GitLabConnector()

# 命令映射表
COMMAND_MAP = {
    "更新代码": {"command": "pull", "args": []},
    "提交修改": {"command": "commit", "args": ["-m", "[MCP]自动提交"]},
    "推送代码": {"command": "push", "args": []},
    "查看状态": {"command": "status", "args": ["-s"]},
    "创建分支": {"command": "checkout", "args": ["-b"]},
    "切换分支": {"command": "checkout", "args": []}
}

def format_date(date_str: str) -> str:
    """格式化日期字符串"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.error(f"日期格式化错误: {str(e)}")
        return date_str

def parse_command(text: str) -> Dict[str, Any]:
    """
    将自然语言转换为Git命令
    
    Args:
        text: 用户输入的自然语言命令
        
    Returns:
        包含命令和参数的字典
    """
    logger.debug(f"解析命令: {text}")
    for keyword, cmd in COMMAND_MAP.items():
        if keyword in text:
            logger.debug(f"找到匹配命令: {cmd}")
            return cmd
    logger.warning(f"未找到匹配命令，使用默认状态命令")
    return {"command": "status", "args": []}  # 默认操作

@mcp.tool()
def git_operation(
    repo_path: str,
    command: str = typer.Option(..., help="支持pull/push/status/checkout等操作")
) -> str:
    """
    执行Git操作
    
    Args:
        repo_path: 仓库路径
        command: Git命令
        
    Returns:
        命令执行结果
    """
    logger.info(f"执行Git操作: {command} 在路径: {repo_path}")
    
    # 检查路径是否在白名单中
    allowed_paths = os.getenv("ALLOWED_PATHS", "").split(",")
    if repo_path not in allowed_paths:
        error_msg = f"错误：路径 {repo_path} 不在允许列表中"
        logger.error(error_msg)
        return error_msg
        
    try:
        # 解析命令
        cmd_info = parse_command(command)
        git_cmd = ["git", "-C", repo_path, cmd_info["command"]] + cmd_info["args"]
        logger.debug(f"执行命令: {' '.join(git_cmd)}")
        
        # 执行命令
        result = subprocess.run(
            git_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"命令执行成功: {result.stdout[:100]}...")
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_msg = f"操作失败: {e.stderr}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"发生错误: {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
def check_collection_commits(
    project_pattern: str = typer.Option("collection", help="项目名称匹配模式"),
    branch: str = typer.Option("master", help="要查看的分支名称")
) -> str:
    """
    查看指定模式的项目分支最近提交记录
    
    Args:
        project_pattern: 项目名称匹配模式
        branch: 分支名称
        
    Returns:
        提交记录信息
    """
    try:
        # 获取所有项目
        projects = gitlab_connector.gl.projects.list(all=True)
        
        # 过滤项目
        filtered_projects = [p for p in projects if project_pattern in p.name]
        
        if not filtered_projects:
            return f"没有找到包含 {project_pattern} 的项目"
            
        result = []
        result.append(f"找到 {len(filtered_projects)} 个匹配的项目:\n")
        
        # 遍历每个项目
        for project in filtered_projects:
            try:
                result.append(f"\n项目: {project.name}")
                result.append(f"URL: {project.web_url}")
                
                # 获取指定分支
                try:
                    branch_info = project.branches.get(branch)
                    result.append(f"分支: {branch_info.name}")
                    
                    # 获取最近一次提交
                    commit = branch_info.commit
                    if isinstance(commit, dict):
                        result.append(f"最近提交: {commit.get('id', '未知')[:8]}")
                        result.append(f"提交信息: {commit.get('message', '未知')}")
                        result.append(f"提交时间: {format_date(commit.get('committed_date', '未知'))}")
                        result.append(f"提交者: {commit.get('author_name', '未知')}")
                    else:
                        result.append(f"最近提交: {commit.id[:8]}")
                        result.append(f"提交信息: {commit.message}")
                        result.append(f"提交时间: {format_date(commit.committed_date)}")
                        result.append(f"提交者: {commit.author_name}")
                    
                except gitlab.exceptions.GitlabGetError:
                    result.append(f"⚠️ 无法获取{branch}分支信息")
                    
            except Exception as e:
                result.append(f"处理项目 {project.name} 时出错: {str(e)}")
                
        return "\n".join(result)
        
    except Exception as e:
        return f"发生错误: {str(e)}"

@mcp.tool()
def list_project_branches(
    project_name: str = typer.Option(..., help="项目名称或路径"),
) -> str:
    """
    列出项目的所有分支
    
    Args:
        project_name: 项目名称或路径
        
    Returns:
        分支列表信息
    """
    try:
        # 获取项目
        project = gitlab_connector.gl.projects.get(project_name)
        
        # 获取所有分支
        branches = project.branches.list()
        
        result = []
        result.append(f"项目 {project.name} 的分支列表:")
        
        for branch in branches:
            result.append(f"\n分支: {branch.name}")
            commit = branch.commit
            if isinstance(commit, dict):
                result.append(f"最近提交: {commit.get('id', '未知')[:8]}")
                result.append(f"提交者: {commit.get('author_name', '未知')}")
                result.append(f"提交时间: {format_date(commit.get('committed_date', '未知'))}")
            else:
                result.append(f"最近提交: {commit.id[:8]}")
                result.append(f"提交者: {commit.author_name}")
                result.append(f"提交时间: {format_date(commit.committed_date)}")
                
        return "\n".join(result)
        
    except gitlab.exceptions.GitlabGetError:
        return f"未找到项目: {project_name}"
    except Exception as e:
        return f"发生错误: {str(e)}"

@mcp.tool()
def create_merge_request(
    project_path: str = typer.Option(..., help="项目路径"),
    source_branch: str = typer.Option(..., help="源分支"),
    target_branch: str = typer.Option("master", help="目标分支"),
    title: str = typer.Option(..., help="合并请求标题"),
    description: str = typer.Option("", help="合并请求描述")
) -> str:
    """
    创建合并请求
    
    Args:
        project_path: 项目路径
        source_branch: 源分支
        target_branch: 目标分支
        title: 合并请求标题
        description: 合并请求描述
        
    Returns:
        合并请求URL或错误信息
    """
    try:
        mr_url = gitlab_connector.create_merge_request(
            project_path=project_path,
            source_branch=source_branch,
            target_branch=target_branch,
            title=title,
            description=description
        )
        
        if mr_url:
            return f"合并请求创建成功: {mr_url}"
        else:
            return "创建合并请求失败"
            
    except Exception as e:
        return f"发生错误: {str(e)}"

def main():
    """启动MCP服务"""
    mcp.run()

if __name__ == "__main__":
    main() 