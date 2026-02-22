#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分类器 - A股深度优化日报系统v2.0.0
功能：对股票进行概念标签、行业标签和策略匹配度分类
作者：OpenClaw AI Assistant
日期：2026-02-19
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
import json
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockClassifier:
    """
    股票分类器类
    负责对股票进行多维度分类：
    1. 概念标签（30+个概念）
    2. 行业标签（20+个行业）
    3. 策略匹配度评估
    """
    
    def __init__(self):
        """初始化分类器"""
        self.concept_tags = self._load_concept_tags()
        self.industry_tags = self._load_industry_tags()
        self.strategy_mapping = self._load_strategy_mapping()
        
    def _load_concept_tags(self) -> Dict[str, List[str]]:
        """
        加载概念标签定义
        返回：概念名称 -> 关键词列表的映射
        """
        concept_tags = {
            # AI相关概念
            "人工智能": ["AI", "人工智能", "机器学习", "深度学习", "神经网络", "大模型", "AIGC"],
            "AI芯片": ["GPU", "AI芯片", "算力芯片", "NPU", "TPU", "ASIC"],
            "大数据": ["大数据", "数据挖掘", "数据分析", "数据处理"],
            "云计算": ["云计算", "云服务", "云平台", "IaaS", "PaaS", "SaaS"],
            
            # 半导体产业链
            "半导体": ["半导体", "芯片", "集成电路", "晶圆", "光刻"],
            "半导体设备": ["光刻机", "刻蚀机", "薄膜沉积", "检测设备"],
            "半导体材料": ["硅片", "光刻胶", "电子气体", "靶材"],
            
            # 新能源
            "光伏": ["光伏", "太阳能", "组件", "逆变器", "硅料"],
            "锂电池": ["锂电池", "动力电池", "储能电池", "正极材料", "负极材料"],
            "新能源车": ["新能源车", "电动车", "电动汽车", "智能汽车"],
            "风电": ["风电", "风能", "风机", "叶片", "塔筒"],
            
            # 金融
            "银行": ["银行", "商业银行", "国有银行", "股份制银行"],
            "保险": ["保险", "寿险", "财险", "再保险"],
            "证券": ["证券", "券商", "投行", "经纪业务"],
            
            # 消费
            "白酒": ["白酒", "高端白酒", "次高端白酒", "酱香型"],
            "医药": ["医药", "创新药", "生物制药", "医疗器械"],
            "消费电子": ["消费电子", "智能手机", "可穿戴设备", "TWS耳机"],
            
            # 基建地产
            "房地产": ["房地产", "地产开发", "商业地产", "住宅地产"],
            "建筑建材": ["水泥", "玻璃", "钢材", "防水材料"],
            "工程机械": ["挖掘机", "起重机", "装载机", "混凝土机械"],
            
            # 其他重要概念
            "军工": ["军工", "航空航天", "导弹", "雷达", "军舰"],
            "数字经济": ["数字经济", "数字产业化", "产业数字化"],
            "专精特新": ["专精特新", "小巨人", "单项冠军"],
            "国企改革": ["国企改革", "央企", "混改", "资产重组"],
            "一带一路": ["一带一路", "海外工程", "基础设施"],
            "碳中和": ["碳中和", "碳达峰", "绿色能源", "环保"],
            "元宇宙": ["元宇宙", "VR", "AR", "虚拟现实", "数字孪生"],
            "Web3": ["Web3", "区块链", "去中心化", "NFT", "DAO"],
            "6G": ["6G", "通信技术", "卫星互联网", "太赫兹"],
            "量子计算": ["量子计算", "量子通信", "量子加密"],
            "脑机接口": ["脑机接口", "神经科技", "BCI"],
            "合成生物": ["合成生物", "基因编辑", "CRISPR"]
        }
        return concept_tags
    
    def _load_industry_tags(self) -> Dict[str, List[str]]:
        """
        加载行业标签定义
        返回：行业名称 -> 关键词列表的映射
        """
        industry_tags = {
            "计算机": ["软件", "IT服务", "系统集成", "信息安全"],
            "电子": ["半导体", "光学光电子", "消费电子", "元件"],
            "通信": ["通信设备", "通信服务", "运营商"],
            "电力设备": ["电网设备", "电源设备", "电机"],
            "汽车": ["乘用车", "商用车", "汽车零部件"],
            "有色金属": ["铜", "铝", "锂", "钴", "稀土"],
            "钢铁": ["普钢", "特钢", "不锈钢"],
            "化工": ["化学制品", "化学原料", "化肥", "农药"],
            "医药生物": ["化学制药", "生物制品", "医疗服务", "医疗器械"],
            "食品饮料": ["白酒", "啤酒", "软饮料", "调味品", "乳制品"],
            "家用电器": ["白色家电", "黑色家电", "小家电"],
            "轻工制造": ["造纸", "包装印刷", "家具", "文娱用品"],
            "纺织服饰": ["服装", "家纺", "鞋帽", "珠宝"],
            "农林牧渔": ["种植业", "畜牧业", "渔业", "饲料"],
            "商贸零售": ["百货", "超市", "专业连锁", "电商"],
            "交通运输": ["航空", "机场", "公路", "铁路", "港口", "物流"],
            "房地产": ["住宅开发", "商业地产", "园区开发"],
            "建筑装饰": ["房屋建设", "装修装饰", "基础建设"],
            "银行": ["国有银行", "股份制银行", "城商行", "农商行"],
            "非银金融": ["证券", "保险", "信托", "期货"]
        }
        return industry_tags
    
    def _load_strategy_mapping(self) -> Dict[str, Dict[str, float]]:
        """
        加载策略匹配映射
        返回：策略名称 -> {概念/行业: 匹配权重} 的映射
        """
        strategy_mapping = {
            # 强势动量策略 (涨幅>7%)
            "强势动量": {
                "人工智能": 0.85,
                "AI芯片": 0.90,
                "半导体": 0.80,
                "新能源车": 0.75,
                "光伏": 0.70,
                "锂电池": 0.75,
                "军工": 0.80,
                "6G": 0.85,
                "元宇宙": 0.70,
                "Web3": 0.65
            },
            # 反转动量策略
            "反转动量": {
                "银行": 0.85,
                "保险": 0.80,
                "白酒": 0.75,
                "医药": 0.70,
                "公用事业": 0.80,
                "高速公路": 0.75,
                "煤炭": 0.70,
                "石油石化": 0.65
            },
            # 突破动量策略
            "突破动量": {
                "半导体设备": 0.90,
                "AI芯片": 0.85,
                "6G": 0.85,
                "量子计算": 0.90,
                "脑机接口": 0.85,
                "合成生物": 0.80,
                "军工": 0.75,
                "新能源车": 0.70
            },
            # 深度价值策略 (PE<15)
            "深度价值": {
                "银行": 0.90,
                "保险": 0.85,
                "煤炭": 0.80,
                "钢铁": 0.75,
                "建材": 0.70,
                "电力": 0.75,
                "高速公路": 0.80,
                "港口": 0.70
            },
            # 合理价值策略 (PE 15-30)
            "合理价值": {
                "食品饮料": 0.80,
                "家用电器": 0.75,
                "医药生物": 0.70,
                "汽车": 0.65,
                "电子": 0.60,
                "计算机": 0.55,
                "通信": 0.60,
                "电力设备": 0.65
            },
            # 质量价值策略 (ROE>15%)
            "质量价值": {
                "白酒": 0.90,
                "食品饮料": 0.85,
                "家用电器": 0.80,
                "医药生物": 0.75,
                "电子": 0.70,
                "计算机": 0.65,
                "银行": 0.60,
                "非银金融": 0.55
            },
            # 抗跌防御策略 (跌幅<1%)
            "抗跌防御": {
                "银行": 0.85,
                "公用事业": 0.80,
                "医药": 0.75,
                "食品饮料": 0.70,
                "高速公路": 0.80,
                "煤炭": 0.75,
                "石油石化": 0.70,
                "黄金": 0.85
            },
            # 稳健防御策略
            "稳健防御": {
                "银行": 0.80,
                "保险": 0.75,
                "公用事业": 0.75,
                "医药": 0.70,
                "食品饮料": 0.65,
                "必需消费品": 0.70,
                "电信": 0.65,
                "房地产": 0.60
            },
            # 红利防御策略
            "红利防御": {
                "银行": 0.90,
                "煤炭": 0.85,
                "石油石化": 0.80,
                "电力": 0.75,
                "高速公路": 0.80,
                "港口": 0.75,
                "钢铁": 0.70,
                "建材": 0.65
            },
            # 军工映射策略
            "军工映射": {
                "军工": 0.95,
                "航空航天": 0.90,
                "半导体": 0.75,
                "通信": 0.70,
                "新材料": 0.65,
                "高端制造": 0.60
            },
            # AI芯片映射策略
            "AI芯片映射": {
                "AI芯片": 0.95,
                "半导体": 0.90,
                "半导体设备": 0.85,
                "半导体材料": 0.80,
                "人工智能": 0.75,
                "云计算": 0.70,
                "大数据": 0.65
            },
            # 新能源映射策略
            "新能源映射": {
                "光伏": 0.90,
                "锂电池": 0.85,
                "新能源车": 0.80,
                "风电": 0.75,
                "氢能": 0.70,
                "储能": 0.65,
                "电网设备": 0.60
            },
            # 消费电子映射策略
            "消费电子映射": {
                "消费电子": 0.90,
                "半导体": 0.75,
                "光学光电子": 0.70,
                "元器件": 0.65,
                "5G": 0.60,
                "物联网": 0.55
            },
            # 生物医药映射策略
            "生物医药映射": {
                "医药": 0.90,
                "创新药": 0.85,
                "生物制药": 0.80,
                "医疗器械": 0.75,
                "医疗服务": 0.70,
                "基因治疗": 0.65,
                "合成生物": 0.60
            }
        }
        return strategy_mapping
    
    def classify_stock_concepts(self, stock_info: Dict[str, str]) -> List[str]:
        """
        对单只股票进行概念分类
        
        Args:
            stock_info: 股票信息字典，包含'name', 'industry', 'business'等字段
            
        Returns:
            匹配的概念标签列表
        """
        matched_concepts = []
        stock_text = f"{stock_info.get('name', '')} {stock_info.get('industry', '')} {stock_info.get('business', '')}".lower()
        
        for concept, keywords in self.concept_tags.items():
            for keyword in keywords:
                if keyword.lower() in stock_text:
                    matched_concepts.append(concept)
                    break
        
        return matched_concepts
    
    def classify_stock_industry(self, stock_info: Dict[str, str]) -> List[str]:
        """
        对单只股票进行行业分类
        
        Args:
            stock_info: 股票信息字典
            
        Returns:
            匹配的行业标签列表
        """
        matched_industries = []
        stock_text = f"{stock_info.get('industry', '')} {stock_info.get('business', '')}".lower()
        
        for industry, keywords in self.industry_tags.items():
            for keyword in keywords:
                if keyword.lower() in stock_text:
                    matched_industries.append(industry)
                    break
        
        return matched_industries
    
    def calculate_strategy_match_score(self, concepts: List[str], industries: List[str], strategy: str) -> float:
        """
        计算股票与特定策略的匹配度
        
        Args:
            concepts: 股票的概念标签列表
            industries: 股票的行业标签列表
            strategy: 策略名称
            
        Returns:
            匹配度分数 (0-1)
        """
        if strategy not in self.strategy_mapping:
            return 0.0
        
        strategy_weights = self.strategy_mapping[strategy]
        max_score = 0.0
        
        # 检查概念匹配
        for concept in concepts:
            if concept in strategy_weights:
                max_score = max(max_score, strategy_weights[concept])
        
        # 检查行业匹配
        for industry in industries:
            if industry in strategy_weights:
                max_score = max(max_score, strategy_weights[industry])
        
        return max_score
    
    def classify_stocks_batch(self, stocks_df: pd.DataFrame) -> pd.DataFrame:
        """
        批量分类股票
        
        Args:
            stocks_df: 股票数据DataFrame，包含'name', 'industry', 'business'等列
            
        Returns:
            带有分类标签和策略匹配度的DataFrame
        """
        results = []
        
        for idx, row in stocks_df.iterrows():
            stock_info = row.to_dict()
            
            # 概念分类
            concepts = self.classify_stock_concepts(stock_info)
            
            # 行业分类
            industries = self.classify_stock_industry(stock_info)
            
            # 计算各策略匹配度
            strategy_scores = {}
            all_strategies = list(self.strategy_mapping.keys())
            for strategy in all_strategies:
                score = self.calculate_strategy_match_score(concepts, industries, strategy)
                strategy_scores[strategy] = score
            
            result_row = {
                'stock_code': row.get('code', ''),
                'stock_name': row.get('name', ''),
                'concepts': concepts,
                'industries': industries,
                **strategy_scores
            }
            results.append(result_row)
        
        return pd.DataFrame(results)
    
    def get_top_stocks_by_strategy(self, classified_stocks_df: pd.DataFrame, strategy: str, top_n: int = 20) -> pd.DataFrame:
        """
        获取特定策略下匹配度最高的股票
        
        Args:
            classified_stocks_df: 已分类的股票DataFrame
            strategy: 策略名称
            top_n: 返回前N只股票
            
        Returns:
            排序后的股票DataFrame
        """
        if strategy not in classified_stocks_df.columns:
            logger.warning(f"Strategy {strategy} not found in DataFrame columns")
            return pd.DataFrame()
        
        sorted_df = classified_stocks_df.sort_values(by=strategy, ascending=False)
        return sorted_df.head(top_n)

def main():
    """测试函数"""
    classifier = StockClassifier()
    
    # 测试数据
    test_stocks = pd.DataFrame([
        {
            'code': '600519',
            'name': '贵州茅台',
            'industry': '食品饮料',
            'business': '白酒生产销售'
        },
        {
            'code': '002475',
            'name': '立讯精密',
            'industry': '电子',
            'business': '消费电子、AI服务器、汽车电子'
        },
        {
            'code': '688981',
            'name': '中芯国际',
            'industry': '半导体',
            'business': '集成电路制造、AI芯片代工'
        }
    ])
    
    # 分类
    classified = classifier.classify_stocks_batch(test_stocks)
    print("股票分类结果:")
    print(classified[['stock_code', 'stock_name', 'concepts', 'industries', 'AI芯片映射', '强势动量']].to_string())
    
    # 获取AI芯片映射策略TOP股票
    ai_chip_top = classifier.get_top_stocks_by_strategy(classified, 'AI芯片映射', 10)
    print("\nAI芯片映射策略TOP股票:")
    print(ai_chip_top[['stock_code', 'stock_name', 'AI芯片映射']].to_string())

if __name__ == "__main__":
    main()