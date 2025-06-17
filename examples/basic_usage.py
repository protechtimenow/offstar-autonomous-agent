#!/usr/bin/env python3
"""Basic OffStar Usage Example"""

import asyncio
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from offstar import OffStarCore

async def main():
    """Demonstrate basic OffStar functionality"""
    
    # Initialize OffStar
    print("🚀 Initializing OffStar...")
    offstar = OffStarCore()
    
    success = await offstar.initialize()
    if not success:
        print("❌ Failed to initialize OffStar")
        return
    
    # Get agent status
    status = await offstar.get_status()
    print(f"\n📊 Agent Status:")
    print(f"Agent ID: {status['agent_id'][:8]}...")
    print(f"Status: {status['status']}")
    print(f"Plugins: {', '.join(status['plugins'])}")
    
    # Example task execution
    print("\n🔍 Executing example tasks...")
    
    # DeFi metrics task
    defi_task = {
        "type": "fetch_protocol_metrics",
        "protocol": "uniswap_v3",
        "plugin_type": "defi"
    }
    
    result = await offstar.execute_task(defi_task)
    print(f"\nDeFi Task Result:")
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        metrics = result['result']
        print(f"TVL: ${float(metrics.tvl):,.0f}")
        print(f"APY: {float(metrics.apy):.1%}")
        print(f"Risk Score: {metrics.risk_score}")
    
    # Yield opportunities task
    yield_task = {
        "type": "calculate_yield_opportunities",
        "plugin_type": "defi"
    }
    
    result = await offstar.execute_task(yield_task)
    print(f"\n💰 Yield Opportunities:")
    if result['status'] == 'success':
        for i, opp in enumerate(result['result'][:3], 1):
            print(f"{i}. {opp['protocol']}: {opp['apy']:.1%} APY (Risk: {opp['risk_score']:.1f})")
    
    # Health check
    print("\n🏥 Performing health checks...")
    for plugin_name in offstar.plugins:
        health = await offstar.plugins[plugin_name].health_check()
        print(f"{plugin_name}: {health['status']} ({health['metrics']['tasks_executed']} tasks)")
    
    print("\n✅ Demo complete!")
    await offstar.shutdown()

if __name__ == "__main__":
    asyncio.run(main())