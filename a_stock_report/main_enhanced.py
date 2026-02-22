#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
"""
A股深度优化日报系统 v2.0.0
主程序入口 - 优化版

功能：
- 策略细分：5大策略 → 15+子策略
- 标的分类：概念标签 + 行业标签系统  
- 交叉研究：概念×策略矩阵、行业×策略矩阵、三维分析
- 案例分析：个股深度分析（以星环科技为例）
- 报告生成：结构化深度报告

作者: OpenClaw AI Assistant
日期: 2026-02-19
"""

import sys
import os
import logging
from datetime import datetime, timedelta

# 添加项目路径到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.strategy_refiner import StrategyRefiner
from scripts.stock_classifier import StockClassifier  
from scripts.cross_analyzer import CrossAnalyzer
from scripts.enhanced_report_generator import EnhancedReportGenerator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('a_stock_report.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class AStockDeepReportSystem:
    """A股深度优化日报系统主类"""
    
    def __init__(self):
        self.strategy_refiner = StrategyRefiner()
        self.stock_classifier = StockClassifier()
        self.cross_analyzer = CrossAnalyzer()
        self.report_generator = EnhancedReportGenerator()
        
        # 创建输出目录
        self.output_dir = "reports"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def run_daily_report(self, date=None):
        """
        生成每日深度优化日报
        
        Args:
            date (str): 日期，格式 YYYY-MM-DD，默认为今天
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        logging.info(f"开始生成 {date} 的A股深度优化日报")
        
        try:
            # 1. 策略细分分析
            logging.info("步骤1: 执行策略细分分析...")
            refined_strategies = self.strategy_refiner.refine_strategies(date)
            
            # 2. 标的分类
            logging.info("步骤2: 执行标的分类...")
            classified_stocks = self.stock_classifier.classify_stocks(date)
            
            # 3. 交叉分析
            logging.info("步骤3: 执行交叉分析...")
            cross_analysis = self.cross_analyzer.perform_cross_analysis(
                refined_strategies, classified_stocks, date
            )
            
            # 4. 生成深度报告
            logging.info("步骤4: 生成深度优化日报...")
            report_content = self.report_generator.generate_enhanced_report(
                refined_strategies, classified_stocks, cross_analysis, date
            )
            
            # 5. 保存报告
            report_filename = f"A股深度优化日报_{date}.md"
            report_path = os.path.join(self.output_dir, report_filename)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
                
            logging.info(f"日报生成完成: {report_path}")
            
            return report_path
            
        except Exception as e:
            logging.error(f"生成日报时发生错误: {str(e)}")
            raise
            
    def analyze_case_study(self, stock_code, stock_name, date=None):
        """
        执行个股案例分析
        
        Args:
            stock_code (str): 股票代码
            stock_name (str): 股票名称  
            date (str): 日期，格式 YYYY-MM-DD，默认为今天
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        logging.info(f"开始个股案例分析: {stock_name}({stock_code}) - {date}")
        
        try:
            # 获取个股详细信息
            stock_info = self.stock_classifier.get_stock_details(stock_code, date)
            
            # 执行三维分析
            three_d_analysis = self.cross_analyzer.perform_three_d_analysis(
                stock_code, stock_name, stock_info, date
            )
            
            # 生成案例分析报告
            case_report = self.report_generator.generate_case_study_report(
                stock_code, stock_name, stock_info, three_d_analysis, date
            )
            
            # 保存案例分析报告
            case_filename = f"个股案例分析_{stock_name}_{date}.md"
            case_path = os.path.join(self.output_dir, case_filename)
            
            with open(case_path, 'w', encoding='utf-8') as f:
                f.write(case_report)
                
            logging.info(f"案例分析完成: {case_path}")
            
            return case_path
            
        except Exception as e:
            logging.error(f"案例分析时发生错误: {str(e)}")
            raise

def main():
    """主函数"""
    system = AStockDeepReportSystem()
    
    # 生成今日日报
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = system.run_daily_report(today)
    
    # 执行星环科技案例分析（示例）
    # 星环科技股票代码假设为688031（实际需要确认）
    case_path = system.analyze_case_study("688031", "星环科技", today)
    
    print(f"A股深度优化日报系统 v2.0.0 运行完成!")
    print(f"日报文件: {report_path}")
    print(f"案例分析: {case_path}")

if __name__ == "__main__":
    main()