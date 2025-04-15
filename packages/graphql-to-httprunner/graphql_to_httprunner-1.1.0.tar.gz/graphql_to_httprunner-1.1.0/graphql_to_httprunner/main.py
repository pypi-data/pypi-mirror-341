#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL Schema to HttpRunner 测试用例转换工具

该模块是GraphQL Schema到HttpRunner测试用例转换工具的主入口。
处理命令行参数，读取GraphQL Schema文件，协调调用解析器和生成器模块。

主要功能：
1. 解析命令行参数，提供友好的命令行界面
2. 读取GraphQL Schema文件或通过内省查询获取Schema
3. 协调调用SchemaParser解析Schema
4. 协调调用TestCaseGenerator生成测试用例
5. 协调调用QueryGenerator生成查询语句列表
"""

import argparse
import sys
import os

from .parser import GraphQLSchemaParser
from .generator import HttpRunnerTestCaseGenerator
from .query_generator import GraphQLQueryGenerator
from .introspection import fetch_schema_from_introspection, IntrospectionQueryError


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='将GraphQL Schema转换为HttpRunner测试用例或查询语句')
    
    # 创建互斥组，schema文件和内省查询URL只能二选一
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('-f', '--schema-file', help='GraphQL Schema文件路径')
    source_group.add_argument('-i', '--introspection-url', help='GraphQL内省查询URL，如http://localhost:9527/graphql')
    
    # 创建互斥组，生成测试用例或查询语句列表
    output_type_group = parser.add_mutually_exclusive_group(required=True)
    output_type_group.add_argument('-t', '--testcases', action='store_true', help='生成HttpRunner测试用例')
    output_type_group.add_argument('-q', '--queries', action='store_true', help='生成GraphQL查询语句列表')
    
    parser.add_argument('-o', '--output', default=None, help='输出目录路径或文件路径')
    parser.add_argument('-u', '--base-url', default='http://localhost:8888', help='GraphQL API基础URL')
    parser.add_argument('-d', '--max-depth', type=int, default=2, help='GraphQL查询嵌套的最大深度，默认为2')
    parser.add_argument('--api', action='store_true', help='生成API层测试用例而非用例层测试用例')
    parser.add_argument('--required', action='store_true', help='只包含必选参数，默认情况下包含所有参数')
    
    args = parser.parse_args()
    
    schema = None
    
    # 设置默认输出路径
    if args.output is None:
        if args.testcases:
            if args.api:
                args.output = 'api'
            else:
                args.output = 'testcases'
        else:
            args.output = 'queries.yml'
    
    # 从Schema文件中读取
    if args.schema_file:
        # 检查Schema文件是否存在
        if not os.path.isfile(args.schema_file):
            print(f"错误：Schema文件 '{args.schema_file}' 不存在")
            sys.exit(1)
        
        # 读取Schema文件
        try:
            with open(args.schema_file, 'r', encoding='utf-8') as f:
                schema_content = f.read()
        except Exception as e:
            print(f"读取Schema文件时出错: {e}")
            sys.exit(1)
        
        # 解析Schema
        print(f"开始解析GraphQL Schema文件: {args.schema_file}")
        try:
            parser = GraphQLSchemaParser(schema_content)
            schema = parser.parse()
        except Exception as e:
            print(f"解析Schema文件时出错: {e}")
            sys.exit(1)
    
    # 通过内省查询获取Schema
    elif args.introspection_url:
        print(f"通过内省查询获取GraphQL Schema: {args.introspection_url}")
        try:
            schema = fetch_schema_from_introspection(args.introspection_url)
        except IntrospectionQueryError as e:
            print(f"内省查询失败: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"获取Schema时出错: {e}")
            sys.exit(1)
    
    # 生成测试用例
    if args.testcases:
        output_type = "API层" if args.api else "用例层"
        print(f"\n开始生成HttpRunner {output_type}测试用例...")
        try:
            generator = HttpRunnerTestCaseGenerator(schema, args.base_url, args.max_depth, args.required)

            if args.api:
                testcase_count = generator.generate_api_test_cases(args.output)
                print(f"\n已生成{testcase_count}个API层测试用例到目录: {args.output}")
            else:
                testcase_count = generator.generate_test_cases(args.output)
                print(f"\n已生成{testcase_count}个用例层测试用例到目录: {args.output}")

        except Exception as e:
            print(f"生成测试用例时出错: {e}")
            sys.exit(1)
    
    # 生成查询语句列表
    elif args.queries:
        print(f"\n开始生成GraphQL查询语句列表...")
        try:
            generator = GraphQLQueryGenerator(schema, args.max_depth)
            queries = generator.generate_queries(args.output)
            query_count = len(queries)
            print(f"\n已生成{query_count}个查询语句到文件: {args.output}")
        except Exception as e:
            print(f"生成查询语句时出错: {e}")
            sys.exit(1)
    
    print(f"使用的最大查询深度: {args.max_depth}")
    if args.testcases:
        print(f"使用的基础URL: {args.base_url}")
        print(f"是否只包含必选参数：{'是' if args.required else '否'}")

if __name__ == '__main__':
    main() 