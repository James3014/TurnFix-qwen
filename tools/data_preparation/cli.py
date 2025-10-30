#!/usr/bin/env python3
"""
資料處理工具 CLI 主入口點 (TOOL-106)

實現各種資料處理工具的命令行接口
"""
import argparse
import sys
import os
from pathlib import Path

# 添加項目根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    parser = argparse.ArgumentParser(description='TurnFix 資料處理工具集 (TOOL-106)')
    subparsers = parser.add_subparsers(dest='command', help='可用的命令')

    # 逐字稿清洗命令 (TOOL-106.1)
    clean_parser = subparsers.add_parser('clean', help='清洗逐字稿文件')
    clean_parser.add_argument('--input', '-i', required=True, help='輸入文件或目錄路徑')
    clean_parser.add_argument('--output', '-o', required=True, help='輸出文件或目錄路徑')
    clean_parser.add_argument('--max-length', '-m', type=int, default=500, help='最大段落長度 (默認為500)')

    # 知識抽取命令 (TOOL-106.2)
    extract_parser = subparsers.add_parser('extract', help='從清洗後的文件中抽取知識')
    extract_parser.add_argument('--input', '-i', required=True, help='輸入文件或目錄路徑')
    extract_parser.add_argument('--output', '-o', required=True, help='輸出文件或目錄路徑')

    # 資料驗證命令 (TOOL-106.3)
    validate_parser = subparsers.add_parser('validate', help='驗證資料品質')
    validate_parser.add_argument('--input', '-i', required=True, help='輸入目錄路徑')
    validate_parser.add_argument('--output', '-o', required=True, help='輸出報告文件路徑')

    # 知識導入命令 (TOOL-106.4)
    import_parser = subparsers.add_parser('import', help='將審核後的知識導入向量數據庫')
    import_parser.add_argument('--input', '-i', required=True, help='審核後知識片段的JSON文件路徑')
    import_parser.add_argument('--report', '-r', help='導出報告文件路徑')

    args = parser.parse_args()

    if args.command == 'clean':
        # 執行逐字稿清洗
        from tools.data_preparation.transcript_cleaner import process_directory, process_file
        if os.path.isfile(args.input):
            success = process_file(args.input, args.output)
            if success:
                print("文件清洗完成")
            else:
                print("文件清洗失敗")
                sys.exit(1)
        elif os.path.isdir(args.input):
            results = process_directory(args.input, args.output)
            print(f"目錄清洗完成: {results['successful']} 成功, {results['failed']} 失敗")
        else:
            print(f"輸入路徑不存在: {args.input}")
            sys.exit(1)

    elif args.command == 'extract':
        # 執行知識抽取
        from tools.data_preparation.knowledge_extractor import process_directory, process_file
        if os.path.isfile(args.input):
            success = process_file(args.input, args.output)
            if success:
                print("知識抽取完成")
            else:
                print("知識抽取失敗")
                sys.exit(1)
        elif os.path.isdir(args.input):
            results = process_directory(args.input, args.output)
            print(f"目錄知識抽取完成: {results['successful']} 成功, {results['failed']} 失敗")
        else:
            print(f"輸入路徑不存在: {args.input}")
            sys.exit(1)

    elif args.command == 'validate':
        # 執行資料驗證
        from tools.data_preparation.data_validator import generate_validation_report
        if not os.path.isdir(args.input):
            print(f"輸入目錄不存在: {args.input}")
            sys.exit(1)
        
        report = generate_validation_report(args.input, args.output)
        print(f"驗證報告已生成: {args.output}")
        print(f"檢查文件數: {report['summary']['total_snippets']}")
        print(f"發現問題數: {report['summary']['total_issues']}")

    elif args.command == 'import':
        # 執行知識導入
        from backend.services.knowledge_import_service import import_approved_knowledge_snippets
        result = import_approved_knowledge_snippets(args.input, args.report)
        
        if result['success']:
            print(f"知識導入成功: {result['imported_count']} 個知識片段已導入")
        else:
            print(f"知識導入失敗: {result.get('error', '未知錯誤')}")
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()