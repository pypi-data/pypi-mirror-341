import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="两数相加")
    parser.add_argument("a", type=int, help="第一个整数")
    parser.add_argument("b", type=int, help="第二个整数")
    args = parser.parse_args()
    print(f"结果: {args.a} + {args.b} = {args.a + args.b}")

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        # 捕获参数解析失败导致的异常 [[10]]
        print("\n参数错误：请输入两个整数参数，例如：uvx choumine-add 3 5")
        sys.exit(1)
