#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉分析器 (Cross Analyzer)
实现概念×策略矩阵、行业×策略矩阵、个股×概念×策略三维分析
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrossAnalyzer:
    """
    交叉分析器类
    负责执行多维度的交叉分析，包括：
    1. 概念 × 策略矩阵分析
    2. 行业 × 策略矩阵分析  
    3. 个股 × 概念 × 策略三维分析
    """
    
    def __init__(self):
        """初始化交叉分析器"""
        self.concept_strategy_matrix = None
        self.industry_strategy_matrix = None
        self.stock_concept_strategy_3d = None
        
    def build_concept_strategy_matrix(self, 
                                   stocks_data: pd.DataFrame,
                                   concepts: List[str],
                                   strategies: List[str]) -> pd.DataFrame:
        """
        构建概念×策略矩阵
        
        Args:
            stocks_data: 股票数据DataFrame，包含股票代码、概念标签、策略匹配度等
            concepts: 概念列表
            strategies: 策略列表
            
        Returns:
            概念×策略矩阵DataFrame
        """
        logger.info("构建概念×策略矩阵...")
        
        # 初始化矩阵
        matrix = pd.DataFrame(0.0, index=concepts, columns=strategies)
        
        # 遍历每只股票，累加策略匹配度到对应的概念-策略单元格
        for _, stock in stocks_data.iterrows():
            stock_concepts = stock.get('concepts', [])
            stock_strategies = stock.get('strategies', {})
            
            for concept in stock_concepts:
                if concept in concepts:
                    for strategy, match_score in stock_strategies.items():
                        if strategy in strategies:
                            matrix.loc[concept, strategy] += match_score
        
        # 归一化处理
        matrix = matrix.div(matrix.sum(axis=1), axis=0).fillna(0)
        
        self.concept_strategy_matrix = matrix
        logger.info(f"概念×策略矩阵构建完成，形状: {matrix.shape}")
        return matrix
    
    def build_industry_strategy_matrix(self,
                                    stocks_data: pd.DataFrame,
                                    industries: List[str],
                                    strategies: List[str]) -> pd.DataFrame:
        """
        构建行业×策略矩阵
        
        Args:
            stocks_data: 股票数据DataFrame
            industries: 行业列表
            strategies: 策略列表
            
        Returns:
            行业×策略矩阵DataFrame
        """
        logger.info("构建行业×策略矩阵...")
        
        # 初始化矩阵
        matrix = pd.DataFrame(0.0, index=industries, columns=strategies)
        
        # 遍历每只股票，累加策略匹配度到对应的行业-策略单元格
        for _, stock in stocks_data.iterrows():
            industry = stock.get('industry', '')
            stock_strategies = stock.get('strategies', {})
            
            if industry in industries:
                for strategy, match_score in stock_strategies.items():
                    if strategy in strategies:
                        matrix.loc[industry, strategy] += match_score
        
        # 归一化处理
        matrix = matrix.div(matrix.sum(axis=1), axis=0).fillna(0)
        
        self.industry_strategy_matrix = matrix
        logger.info(f"行业×策略矩阵构建完成，形状: {matrix.shape}")
        return matrix
    
    def build_stock_concept_strategy_3d(self,
                                      stocks_data: pd.DataFrame,
                                      top_n: int = 20) -> Dict:
        """
        构建个股×概念×策略三维分析
        
        Args:
            stocks_data: 股票数据DataFrame
            top_n: 返回前N个最佳匹配的个股
            
        Returns:
            三维分析结果字典
        """
        logger.info("构建个股×概念×策略三维分析...")
        
        # 计算综合评分
        analysis_results = []
        
        for _, stock in stocks_data.iterrows():
            stock_code = stock.get('code', '')
            stock_name = stock.get('name', '')
            concepts = stock.get('concepts', [])
            strategies = stock.get('strategies', {})
            base_score = stock.get('base_score', 0.0)
            
            # 计算概念-策略组合的最佳匹配
            best_combinations = []
            for concept in concepts:
                for strategy, match_score in strategies.items():
                    combined_score = base_score * match_score
                    best_combinations.append({
                        'concept': concept,
                        'strategy': strategy,
                        'match_score': match_score,
                        'combined_score': combined_score
                    })
            
            # 按综合评分排序，取最高分的组合
            if best_combinations:
                best_combinations.sort(key=lambda x: x['combined_score'], reverse=True)
                best_combo = best_combinations[0]
                
                analysis_results.append({
                    'code': stock_code,
                    'name': stock_name,
                    'industry': stock.get('industry', ''),
                    'concepts': concepts,
                    'strategies': strategies,
                    'base_score': base_score,
                    'best_concept': best_combo['concept'],
                    'best_strategy': best_combo['strategy'],
                    'best_match_score': best_combo['match_score'],
                    'best_combined_score': best_combo['combined_score']
                })
        
        # 按综合评分排序，取前N个
        analysis_results.sort(key=lambda x: x['best_combined_score'], reverse=True)
        top_results = analysis_results[:top_n]
        
        self.stock_concept_strategy_3d = {
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'total_stocks_analyzed': len(analysis_results),
            'top_stocks': top_results
        }
        
        logger.info(f"三维分析完成，分析了{len(analysis_results)}只股票，返回前{top_n}只")
        return self.stock_concept_strategy_3d
    
    def get_concept_strategy_insights(self) -> Dict:
        """
        获取概念×策略矩阵的洞察
        
        Returns:
            洞察字典
        """
        if self.concept_strategy_matrix is None:
            logger.warning("概念×策略矩阵未构建")
            return {}
        
        insights = {
            'strongest_concept_strategy_pairs': [],
            'weakest_concept_strategy_pairs': [],
            'concept_diversity_scores': {},
            'strategy_concentration_scores': {}
        }
        
        # 找出最强和最弱的概念-策略对
        matrix_flat = self.concept_strategy_matrix.stack()
        strongest_pairs = matrix_flat.nlargest(5)
        weakest_pairs = matrix_flat.nsmallest(5)
        
        for (concept, strategy), score in strongest_pairs.items():
            insights['strongest_concept_strategy_pairs'].append({
                'concept': concept,
                'strategy': strategy,
                'score': score
            })
        
        for (concept, strategy), score in weakest_pairs.items():
            insights['weakest_concept_strategy_pairs'].append({
                'concept': concept,
                'strategy': strategy,
                'score': score
            })
        
        # 计算概念多样性得分（熵值）
        for concept in self.concept_strategy_matrix.index:
            scores = self.concept_strategy_matrix.loc[concept]
            if scores.sum() > 0:
                normalized_scores = scores / scores.sum()
                entropy = -np.sum(normalized_scores * np.log(normalized_scores + 1e-10))
                insights['concept_diversity_scores'][concept] = entropy
        
        # 计算策略集中度得分
        for strategy in self.concept_strategy_matrix.columns:
            scores = self.concept_strategy_matrix[strategy]
            if scores.sum() > 0:
                concentration = scores.max() / scores.sum()
                insights['strategy_concentration_scores'][strategy] = concentration
        
        return insights
    
    def get_industry_strategy_insights(self) -> Dict:
        """
        获取行业×策略矩阵的洞察
        
        Returns:
            洞察字典
        """
        if self.industry_strategy_matrix is None:
            logger.warning("行业×策略矩阵未构建")
            return {}
        
        insights = {
            'strongest_industry_strategy_pairs': [],
            'weakest_industry_strategy_pairs': [],
            'industry_diversity_scores': {},
            'strategy_industry_concentration': {}
        }
        
        # 找出最强和最弱的行业-策略对
        matrix_flat = self.industry_strategy_matrix.stack()
        strongest_pairs = matrix_flat.nlargest(5)
        weakest_pairs = matrix_flat.nsmallest(5)
        
        for (industry, strategy), score in strongest_pairs.items():
            insights['strongest_industry_strategy_pairs'].append({
                'industry': industry,
                'strategy': strategy,
                'score': score
            })
        
        for (industry, strategy), score in weakest_pairs.items():
            insights['weakest_industry_strategy_pairs'].append({
                'industry': industry,
                'strategy': strategy,
                'score': score
            })
        
        # 计算行业多样性得分
        for industry in self.industry_strategy_matrix.index:
            scores = self.industry_strategy_matrix.loc[industry]
            if scores.sum() > 0:
                normalized_scores = scores / scores.sum()
                entropy = -np.sum(normalized_scores * np.log(normalized_scores + 1e-10))
                insights['industry_diversity_scores'][industry] = entropy
        
        # 计算策略在行业中的集中度
        for strategy in self.industry_strategy_matrix.columns:
            scores = self.industry_strategy_matrix[strategy]
            if scores.sum() > 0:
                concentration = scores.max() / scores.sum()
                insights['strategy_industry_concentration'][strategy] = concentration
        
        return insights
    
    def generate_cross_analysis_report(self) -> str:
        """
        生成交叉分析报告
        
        Returns:
            报告字符串
        """
        report = []
        report.append("# A股深度优化日报 - 交叉分析报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 概念×策略矩阵分析
        if self.concept_strategy_matrix is not None:
            report.append("## 概念×策略矩阵分析")
            report.append("")
            
            insights = self.get_concept_strategy_insights()
            
            report.append("### 最强概念-策略组合")
            for pair in insights['strongest_concept_strategy_pairs']:
                report.append(f"- **{pair['concept']} × {pair['strategy']}**: {pair['score']:.4f}")
            report.append("")
            
            report.append("### 概念多样性分析")
            diverse_concepts = sorted(insights['concept_diversity_scores'].items(), 
                                    key=lambda x: x[1], reverse=True)[:5]
            for concept, diversity in diverse_concepts:
                report.append(f"- **{concept}**: 多样性得分 {diversity:.4f}")
            report.append("")
        
        # 行业×策略矩阵分析
        if self.industry_strategy_matrix is not None:
            report.append("## 行业×策略矩阵分析")
            report.append("")
            
            insights = self.get_industry_strategy_insights()
            
            report.append("### 最强行业-策略组合")
            for pair in insights['strongest_industry_strategy_pairs']:
                report.append(f"- **{pair['industry']} × {pair['strategy']}**: {pair['score']:.4f}")
            report.append("")
            
            report.append("### 行业多样性分析")
            diverse_industries = sorted(insights['industry_diversity_scores'].items(), 
                                      key=lambda x: x[1], reverse=True)[:5]
            for industry, diversity in diverse_industries:
                report.append(f"- **{industry}**: 多样性得分 {diversity:.4f}")
            report.append("")
        
        # 个股三维分析
        if self.stock_concept_strategy_3d is not None:
            report.append("## 个股×概念×策略三维分析 (TOP 20)")
            report.append("")
            
            for i, stock in enumerate(self.stock_concept_strategy_3d['top_stocks'], 1):
                report.append(f"### {i}. {stock['name']} ({stock['code']})")
                report.append(f"- **所属行业**: {stock['industry']}")
                report.append(f"- **核心概念**: {stock['best_concept']}")
                report.append(f"- **最佳策略**: {stock['best_strategy']}")
                report.append(f"- **策略匹配度**: {stock['best_match_score']:.4f}")
                report.append(f"- **综合评分**: {stock['best_combined_score']:.4f}")
                report.append("")
        
        return "\n".join(report)

def main():
    """测试函数"""
    # 创建示例数据
    sample_data = pd.DataFrame({
        'code': ['000001', '600000', '300750'],
        'name': ['平安银行', '浦发银行', '宁德时代'],
        'industry': ['银行', '银行', '电池'],
        'concepts': [['金融科技', '银行'], ['金融科技', '银行'], ['新能源', '电池', '锂电池']],
        'strategies': [
            {'强势动量': 0.62, '红利防御': 0.72},
            {'强势动量': 0.58, '红利防御': 0.68},
            {'AI芯片映射': 0.58, '强势动量': 0.65}
        ],
        'base_score': [0.85, 0.78, 0.92]
    })
    
    # 初始化交叉分析器
    analyzer = CrossAnalyzer()
    
    # 构建矩阵
    concepts = ['金融科技', '银行', '新能源', '电池', '锂电池']
    strategies = ['强势动量', '红利防御', '深度价值', 'AI芯片映射']
    
    analyzer.build_concept_strategy_matrix(sample_data, concepts, strategies)
    analyzer.build_industry_strategy_matrix(sample_data, ['银行', '电池'], strategies)
    analyzer.build_stock_concept_strategy_3d(sample_data, top_n=3)
    
    # 生成报告
    report = analyzer.generate_cross_analysis_report()
    print(report)

if __name__ == "__main__":
    main()