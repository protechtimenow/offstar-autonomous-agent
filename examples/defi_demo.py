#!/usr/bin/env python3
"""Advanced DeFi Analytics Demo"""

import asyncio
import sys
import os
from datetime import datetime

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from offstar import OffStarCore

async def run_defi_analysis():
    """Comprehensive DeFi analysis demonstration"""
    
    print("🔥 OffStar DeFi Analytics Demo")
    print("=" * 50)
    
    # Initialize OffStar
    offstar = OffStarCore()
    await offstar.initialize()
    
    defi_plugin = offstar.plugins['defi']
    
    print("\n📊 Fetching Protocol Metrics...")
    protocols = ['uniswap_v3', 'aave_v3', 'compound_v3']
    
    for protocol in protocols:
        try:
            metrics = await defi_plugin.fetch_protocol_metrics(protocol)
            print(f"\n{protocol.upper().replace('_', ' ')}:")
            print(f"├── TVL: ${float(metrics.tvl):,.0f}")
            print(f"├── 24h Volume: ${float(metrics.volume_24h):,.0f}")
            print(f"├── APY: {float(metrics.apy):.1%}")
            print(f"└── Risk Score: {metrics.risk_score:.1f}/10")
            
        except Exception as e:
            print(f"❌ Error fetching {protocol} metrics: {e}")
    
    print("\n💎 Calculating Yield Opportunities...")
    
    try:
        opportunities = await defi_plugin.calculate_yield_opportunities()
        print("\nTop Yield Opportunities (Risk-Adjusted):")
        
        for i, opp in enumerate(opportunities, 1):
            print(f"\n{i}. {opp['protocol'].upper().replace('_', ' ')}")
            print(f"├── APY: {opp['apy']:.1%}")
            print(f"├── Risk Score: {opp['risk_score']:.1f}")
            print(f"├── Risk-Adjusted Yield: {opp['risk_adjusted_yield']:.2%}")
            print(f"└── TVL: ${opp['tvl']:,.0f}")
            
    except Exception as e:
        print(f"❌ Error calculating opportunities: {e}")
    
    print("\n🏥 Protocol Health Monitoring...")
    
    try:
        health_report = await defi_plugin.monitor_protocol_health()
        
        for protocol, health in health_report['protocols'].items():
            status_emoji = {
                'healthy': '🟢',
                'warning': '🟡', 
                'critical': '🔴',
                'error': '❌'
            }.get(health.get('status', 'error'), '❓')
            
            print(f"\n{status_emoji} {protocol.upper().replace('_', ' ')}")
            
            if 'health_score' in health:
                print(f"├── Health Score: {health['health_score']:.0f}/100")
                print(f"├── Status: {health['status'].upper()}")
                print(f"├── TVL: ${health['tvl']:,.0f}")
                print(f"└── APY: {health['apy']:.1%}")
            else:
                print(f"└── Error: {health.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"❌ Error monitoring health: {e}")
    
    # Plugin health check
    print("\n🔧 Plugin Diagnostics...")
    plugin_health = await defi_plugin.health_check()
    
    print(f"Plugin: {plugin_health['name']} v{plugin_health['version']}")
    print(f"Status: {plugin_health['status'].upper()}")
    print(f"Tasks Executed: {plugin_health['metrics']['tasks_executed']}")
    print(f"Error Count: {plugin_health['error_count']}")
    print(f"Avg Execution Time: {plugin_health['metrics']['avg_execution_time']:.3f}s")
    
    if plugin_health['recent_errors']:
        print("Recent Errors:")
        for error in plugin_health['recent_errors'][-3:]:
            print(f"  • {error}")
    
    print("\n" + "=" * 50)
    print("🎯 Analysis Complete")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    await offstar.shutdown()

if __name__ == "__main__":
    asyncio.run(run_defi_analysis())