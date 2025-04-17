"""
GitLab连接模块 - 提供GitLab API的封装和认证管理
"""

from typing import Optional, Dict, Any
import os
import logging
from pathlib import Path
from gitlab import Gitlab
from gitlab.exceptions import GitlabError, GitlabAuthenticationError

# 配置日志目录
log_dir = os.path.join(str(Path.home()), '.local', 'share', 'gitlab_mcp')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'gitlab_mcp.log')

# 配置日志
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "DEBUG"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GitLabConnector:
    """GitLab连接器类，封装GitLab API操作"""
    
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None, test_mode: bool = False):
        """
        初始化GitLab连接器
        
        Args:
            base_url: GitLab服务器地址，如果为None则从环境变量获取
            token: GitLab访问令牌，如果为None则从环境变量获取
            test_mode: 是否为测试模式，在测试模式下不会真正连接GitLab服务器
        """
        self.base_url = base_url or os.getenv("GITLAB_API_BASE")
        self.token = token or os.getenv("GITLAB_ACCESS_TOKEN")
        self.test_mode = test_mode
        
        if not self.base_url or not self.token:
            error_msg = "GitLab配置错误：\n"
            if not self.base_url:
                error_msg += "- GITLAB_API_BASE 环境变量未设置\n"
            if not self.token:
                error_msg += "- GITLAB_ACCESS_TOKEN 环境变量未设置\n"
            error_msg += "\n请在环境变量中设置这些值。"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if not self.test_mode:
            try:
                self.gl = Gitlab(self.base_url, private_token=self.token, ssl_verify=False)
                # 测试连接
                self.gl.auth()
                logger.info(f"成功连接到GitLab服务器: {self.base_url}")
            except GitlabAuthenticationError as e:
                error_msg = f"GitLab认证失败: {str(e)}\n请检查 GITLAB_ACCESS_TOKEN 是否正确。"
                logger.error(error_msg)
                raise GitlabAuthenticationError(error_msg)
            except Exception as e:
                error_msg = f"连接GitLab服务器失败: {str(e)}\n请检查 GITLAB_API_BASE 是否正确。"
                logger.error(error_msg)
                raise
            
    def test_connection(self) -> bool:
        """
        测试GitLab连接是否正常
        
        Returns:
            bool: 连接是否成功
        """
        if self.test_mode:
            return True
            
        try:
            self.gl.auth()
            return True
        except Exception as e:
            logger.error(f"GitLab连接测试失败: {str(e)}")
            return False
            
    def get_project(self, project_path: str) -> Optional[Dict[str, Any]]:
        """
        根据项目路径获取项目信息
        
        Args:
            project_path: 项目路径，格式为"namespace/project"
            
        Returns:
            项目信息字典，如果获取失败则返回None
        """
        if self.test_mode:
            return {"id": 1, "name": "test", "path": project_path}
            
        try:
            project = self.gl.projects.get(project_path)
            logger.info(f"成功获取项目: {project_path}")
            return project.attributes
        except GitlabError as e:
            logger.error(f"获取项目失败: {str(e)}")
            return None
            
    def create_merge_request(self, project_path: str, source_branch: str, 
                           target_branch: str, title: str, description: str = "") -> Optional[str]:
        """
        创建合并请求
        
        Args:
            project_path: 项目路径
            source_branch: 源分支
            target_branch: 目标分支
            title: 合并请求标题
            description: 合并请求描述
            
        Returns:
            合并请求的URL，如果创建失败则返回None
        """
        if self.test_mode:
            return f"http://test-gitlab.com/merge/1"
            
        try:
            project = self.gl.projects.get(project_path)
            mr = project.mergerequests.create({
                'source_branch': source_branch,
                'target_branch': target_branch,
                'title': title,
                'description': description
            })
            logger.info(f"成功创建合并请求: {mr.web_url}")
            return mr.web_url
        except GitlabError as e:
            logger.error(f"创建合并请求失败: {str(e)}")
            return None
            
    def get_branches(self, project_path: str) -> Optional[list]:
        """
        获取项目分支列表
        
        Args:
            project_path: 项目路径
            
        Returns:
            分支列表，如果获取失败则返回None
        """
        if self.test_mode:
            return ["master", "develop", "feature/test"]
            
        try:
            project = self.gl.projects.get(project_path)
            branches = [branch.name for branch in project.branches.list()]
            logger.info(f"成功获取分支列表: {project_path}")
            return branches
        except GitlabError as e:
            logger.error(f"获取分支列表失败: {str(e)}")
            return None 