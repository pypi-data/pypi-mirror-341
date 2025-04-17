import argparse
import enum
import sys
import pytest

def main_run(pytest_args: list) -> enum.IntEnum:
    """Run pytest with given arguments
    
    Args:
        pytest_args: List of arguments to pass to pytest
        
    Returns:
        pytest.ExitCode enum value
    """
    print("Running pytest with args:", pytest_args)
    return pytest.main(pytest_args)

def main():
    """API test: parse command line options and run commands."""
    # 主解析器
    parser = argparse.ArgumentParser(description="Run tests with Allure reporting")
    
    # 添加必选参数
    parser.add_argument("--env", required=True, help="Test environment")
    parser.add_argument("--app", required=True, help="Application ID")
    parser.add_argument("--service", required=True, help="Service name")
    parser.add_argument("--project", required=True, help="Project name")
    
    # 解析参数，分离已知参数和要传递给pytest的参数
    args, pytest_args = parser.parse_known_args()
    
    # 打印调试信息
    print("Tool arguments:")
    print(vars(args))
    print("Pytest arguments:", pytest_args)
    
    # 将工具参数转换为pytest可用的格式
    pytest_args.extend([
        f"--env={args.env}",
        f"--app={args.app}",
        f"--service={args.service}",
        f"--project={args.project}"
    ])
    
    # 运行测试
    return_code = main_run(pytest_args)
    
    # 返回退出码
    sys.exit(return_code)
def main_run_alias():
    """ command alias
        prun = pastor run
    """
    main()
if __name__ == "__main__":
    main()