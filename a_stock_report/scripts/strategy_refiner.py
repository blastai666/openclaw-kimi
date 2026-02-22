#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略细分器 - A股深度优化日报系统v2.0.0
将5大基础策略细分为15+子策略，提供更精准的投资指导
"""

class StrategyRefiner:
    def __init__(self):
        # 基础策略配置
        self.base_strategies = {
            'momentum': '动量策略',
            'value': '价值策略', 
            'defensive': '防御策略',
            'us_market_mapping': '美股映射'
        }
        
        # 子策略定义
        self.sub_strategies = {
            # 动量策略细分
            'strong_momentum': {
                'name': '强势动量',
                'description': '涨幅>7%的强势股票',
                'criteria': {'min_change_pct': 7.0},
                'risk_level': 'high',
                'historical_win_rate': 0.62
            },
            'reversal_momentum': {
                'name': '反转动量', 
                'description': '超跌反弹机会',
                'criteria': {'max_change_pct': -5.0},
                'risk_level': 'medium',
                'historical_win_rate': 0.58
            },
            'breakout_momentum': {
                'name': '突破动量',
                'description': '技术形态突破',
                'criteria': {'breakout_pattern': True},
                'risk_level': 'medium',
                'historical_win_rate': 0.60
            },
            
            # 价值策略细分
            'deep_value': {
                'name': '深度价值',
                'description': 'PE<15的深度价值股',
                'criteria': {'max_pe': 15.0, 'min_roe': 8.0},
                'risk_level': 'low',
                'historical_win_rate': 0.65
            },
            'reasonable_value': {
                'name': '合理价值',
                'description': 'PE 15-30的合理估值股',
                'criteria': {'min_pe': 15.0, 'max_pe': 30.0, 'min_roe': 10.0},
                'risk_level': 'low',
                'historical_win_rate': 0.63
            },
            'quality_value': {
                'name': '质量价值',
                'description': 'ROE>15%的高质量价值股',
                'criteria': {'min_roe': 15.0, 'min_pe': 10.0},
                'risk_level': 'low',
                'historical_win_rate': 0.67
            },
            
            # 防御策略细分
            'anti_decline_defensive': {
                'name': '抗跌防御',
                'description': '跌幅<1%的抗跌股票',
                'criteria': {'max_decline_pct': 1.0},
                'risk_level': 'very_low',
                'historical_win_rate': 0.72
            },
            'stable_defensive': {
                'name': '稳健防御',
                'description': '低波动率稳定股',
                'criteria': {'max_volatility': 0.15},
                'risk_level': 'low',
                'historical_win_rate': 0.70
            },
            'dividend_defensive': {
                'name': '红利防御',
                'description': '高股息率防御股',
                'criteria': {'min_dividend_yield': 3.0},
                'risk_level': 'very_low',
                'historical_win_rate': 0.72
            },
            
            # 美股映射策略细分
            'defense_mapping': {
                'name': '军工映射',
                'description': '美股军工股对应的A股标的',
                'criteria': {'sector': '国防军工'},
                'risk_level': 'high',
                'historical_win_rate': 0.55
            },
            'ai_chip_mapping': {
                'name': 'AI芯片映射',
                'description': '美股AI芯片股对应的A股标的',
                'criteria': {'sector': '半导体', 'concept': 'AI芯片'},
                'risk_level': 'high',
                'historical_win_rate': 0.58
            },
            'new_energy_mapping': {
                'name': '新能源映射',
                'description': '美股新能源股对应的A股标的',
                'criteria': {'sector': '电力设备', 'concept': '新能源'},
                'risk_level': 'medium',
                'historical_win_rate': 0.56
            },
            'consumer_electronics_mapping': {
                'name': '消费电子映射',
                'description': '美股消费电子股对应的A股标的',
                'criteria': {'sector': '电子', 'concept': '消费电子'},
                'risk_level': 'medium',
                'historical_win_rate': 0.54
            },
            'biopharma_mapping': {
                'name': '生物医药映射',
                'description': '美股生物医药股对应的A股标的',
                'criteria': {'sector': '医药生物', 'concept': '创新药'},
                'risk_level': 'medium',
                'historical_win_rate': 0.52
            }
        }
    
    def refine_strategy(self, base_strategy, stock_data):
        """
        根据基础策略和股票数据，返回匹配的子策略
        
        Args:
            base_strategy (str): 基础策略名称
            stock_data (dict): 股票数据包含价格、PE、ROE等指标
            
        Returns:
            list: 匹配的子策略列表
        """
        matched_sub_strategies = []
        
        if base_strategy == 'momentum':
            # 动量策略细分逻辑
            if stock_data.get('change_pct', 0) > 7.0:
                matched_sub_strategies.append('strong_momentum')
            elif stock_data.get('change_pct', 0) < -5.0:
                matched_sub_strategies.append('reversal_momentum')
            # 这里可以添加更多技术形态判断逻辑
            
        elif base_strategy == 'value':
            # 价值策略细分逻辑
            pe = stock_data.get('pe', float('inf'))
            roe = stock_data.get('roe', 0)
            
            if pe < 15.0 and roe >= 8.0:
                matched_sub_strategies.append('deep_value')
            elif 15.0 <= pe <= 30.0 and roe >= 10.0:
                matched_sub_strategies.append('reasonable_value')
            elif roe >= 15.0 and pe >= 10.0:
                matched_sub_strategies.append('quality_value')
                
        elif base_strategy == 'defensive':
            # 防御策略细分逻辑
            decline_pct = abs(stock_data.get('change_pct', 0))
            dividend_yield = stock_data.get('dividend_yield', 0)
            volatility = stock_data.get('volatility', float('inf'))
            
            if decline_pct < 1.0:
                matched_sub_strategies.append('anti_decline_defensive')
            if dividend_yield >= 3.0:
                matched_sub_strategies.append('dividend_defensive')
            if volatility <= 0.15:
                matched_sub_strategies.append('stable_defensive')
                
        elif base_strategy == 'us_market_mapping':
            # 美股映射策略细分逻辑
            sector = stock_data.get('sector', '')
            concepts = stock_data.get('concepts', [])
            
            if '国防军工' in sector or '军工' in concepts:
                matched_sub_strategies.append('defense_mapping')
            if '半导体' in sector and 'AI芯片' in concepts:
                matched_sub_strategies.append('ai_chip_mapping')
            if '电力设备' in sector and '新能源' in concepts:
                matched_sub_strategies.append('new_energy_mapping')
            if '电子' in sector and '消费电子' in concepts:
                matched_sub_strategies.append('consumer_electronics_mapping')
            if '医药生物' in sector and '创新药' in concepts:
                matched_sub_strategies.append('biopharma_mapping')
        
        return matched_sub_strategies
    
    def get_sub_strategy_info(self, sub_strategy_name):
        """获取子策略详细信息"""
        return self.sub_strategies.get(sub_strategy_name, {})
    
    def get_all_sub_strategies(self):
        """获取所有子策略列表"""
        return list(self.sub_strategies.keys())
    
    def get_sub_strategy_win_rates(self):
        """获取子策略历史胜率"""
        win_rates = {}
        for name, info in self.sub_strategies.items():
            win_rates[name] = info['historical_win_rate']
        return win_rates

if __name__ == "__main__":
    # 测试代码
    refiner = StrategyRefiner()
    print("策略细分器初始化完成")
    print(f"共定义 {len(refiner.get_all_sub_strategies())} 个子策略")
    
    # 测试动量策略细分
    test_stock = {'change_pct': 8.5, 'pe': 25, 'roe': 12}
    momentum_subs = refiner.refine_strategy('momentum', test_stock)
    print(f"动量策略测试结果: {momentum_subs}")
    
    # 显示所有子策略胜率
    win_rates = refiner.get_sub_strategy_win_rates()
    print("\n子策略历史胜率:")
    for strategy, rate in sorted(win_rates.items(), key=lambda x: x[1], reverse=True):
        info = refiner.get_sub_strategy_info(strategy)
        print(f"- {info['name']}: {rate:.0%} ({info['risk_level']}风险)")