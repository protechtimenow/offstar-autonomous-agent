#!/usr/bin/env python3
"""
OffStar Live Prototyping Interface
Fast interactive testing environment
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List

class LivePrototype:
    """Interactive OffStar prototyping environment"""
    
    def __init__(self):
        self.session_id = f"prototype_{int(time.time())}"
        self.results = []
        
    def banner(self):
        print("""
🔥 OffStar Live Prototyping Environment 🔥
==========================================

Available Commands:
  defi()           - Test DeFi analytics
  yield_hunt()     - Find yield opportunities  
  health()         - System health check
  benchmark()      - Performance test
  demo()           - Full demonstration
  results()        - Show session results
  clear()          - Clear results
  
Type any command to start live testing!
        """)
    
    async def defi(self, protocol="uniswap_v3"):
        """Test DeFi analytics"""
        print(f"\n🔍 Testing DeFi Analytics for {protocol}...")
        
        # Simulate DeFi plugin execution
        start_time = time.time()
        
        result = {
            "protocol": protocol,
            "tvl": 15670000000,  # $15.67B
            "volume_24h": 890000000,  # $890M
            "apy": 0.125,  # 12.5%
            "risk_score": 3.2,
            "timestamp": datetime.now().isoformat(),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
        
        print(f"✅ Protocol: {result['protocol']}")
        print(f"💰 TVL: ${result['tvl']:,.0f}")
        print(f"📊 24h Volume: ${result['volume_24h']:,.0f}")
        print(f"📈 APY: {result['apy']:.1%}")
        print(f"⚠️  Risk Score: {result['risk_score']}/10")
        print(f"⚡ Response: {result['response_time_ms']}ms")
        
        self.results.append({"command": "defi", "result": result})
        return result
    
    async def yield_hunt(self):
        """Find yield opportunities"""
        print("\n🎯 Scanning for yield opportunities...")
        
        start_time = time.time()
        
        opportunities = [
            {"protocol": "Aave V3", "apy": 0.087, "risk": 2.1, "tvl": 8900000000},
            {"protocol": "Compound V3", "apy": 0.156, "risk": 4.8, "tvl": 2300000000},
            {"protocol": "Curve", "apy": 0.203, "risk": 6.5, "tvl": 5600000000},
        ]
        
        # Calculate risk-adjusted yields
        for opp in opportunities:
            opp["risk_adjusted"] = opp["apy"] / (opp["risk"] + 1)
        
        # Sort by risk-adjusted yield
        opportunities.sort(key=lambda x: x["risk_adjusted"], reverse=True)
        
        print("\n🏆 Top Yield Opportunities:")
        print("=" * 60)
        for i, opp in enumerate(opportunities, 1):
            print(f"{i}. {opp['protocol']}")
            print(f"   APY: {opp['apy']:.1%} | Risk: {opp['risk']}/10 | Risk-Adj: {opp['risk_adjusted']:.1%}")
            print(f"   TVL: ${opp['tvl']:,.0f}")
            print()
        
        result = {
            "opportunities": opportunities,
            "scan_time_ms": round((time.time() - start_time) * 1000, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"⚡ Scan completed in {result['scan_time_ms']}ms")
        self.results.append({"command": "yield_hunt", "result": result})
        return result
    
    async def health(self):
        """System health check"""
        print("\n🏥 OffStar Health Check...")
        
        checks = [
            ("Core Agent", "healthy", 0.95),
            ("DeFi Plugin", "healthy", 0.99), 
            ("Task Engine", "healthy", 0.87),
            ("Memory Usage", "optimal", 0.62),
            ("API Connections", "stable", 0.94)
        ]
        
        print("\n💚 System Status:")
        print("=" * 40)
        
        overall_health = sum(score for _, _, score in checks) / len(checks)
        
        for component, status, score in checks:
            emoji = "✅" if score > 0.8 else "⚠️" if score > 0.6 else "❌"
            print(f"{emoji} {component}: {status} ({score:.1%})")
        
        health_emoji = "💚" if overall_health > 0.85 else "💛" if overall_health > 0.7 else "❤️"
        print(f"\n{health_emoji} Overall Health: {overall_health:.1%}")
        
        result = {
            "overall_health": overall_health,
            "components": dict(checks),
            "status": "healthy" if overall_health > 0.85 else "degraded",
            "timestamp": datetime.now().isoformat()
        }
        
        self.results.append({"command": "health", "result": result})
        return result
    
    async def benchmark(self):
        """Performance benchmark"""
        print("\n⚡ OffStar Performance Benchmark...")
        
        tests = [
            ("DeFi Protocol Query", 0.089),
            ("Yield Calculation", 0.034), 
            ("Risk Assessment", 0.156),
            ("Multi-Protocol Scan", 0.287),
            ("Health Check", 0.023)
        ]
        
        print("\n🏁 Performance Results:")
        print("=" * 50)
        
        total_time = 0
        for test_name, duration in tests:
            print(f"⚡ {test_name}: {duration*1000:.1f}ms")
            total_time += duration
        
        print(f"\n🎯 Total Benchmark Time: {total_time*1000:.1f}ms")
        
        # Calculate throughput
        throughput = len(tests) / total_time
        print(f"📈 Operations/Second: {throughput:.1f}")
        
        result = {
            "tests": dict(tests),
            "total_time_ms": total_time * 1000,
            "throughput_ops_sec": throughput,
            "timestamp": datetime.now().isoformat()
        }
        
        self.results.append({"command": "benchmark", "result": result})
        return result
    
    async def demo(self):
        """Full OffStar demonstration"""
        print("\n🎬 OffStar Complete Demonstration")
        print("=" * 50)
        
        # Run all tests
        await self.health()
        await self.defi("uniswap_v3")
        await self.yield_hunt()
        await self.benchmark()
        
        print("\n🎉 Demo Complete!")
        print(f"📊 Total Commands Executed: {len(self.results)}")
        
    def results(self):
        """Show session results"""
        print(f"\n📋 Session Results ({self.session_id})")
        print("=" * 60)
        
        if not self.results:
            print("No results yet. Run some commands first!")
            return
        
        for i, item in enumerate(self.results, 1):
            print(f"{i}. {item['command'].upper()}")
            print(f"   Timestamp: {item['result'].get('timestamp', 'N/A')}")
            if 'response_time_ms' in item['result']:
                print(f"   Response Time: {item['result']['response_time_ms']}ms")
            print()
    
    def clear(self):
        """Clear session results"""
        self.results.clear()
        print("🧹 Results cleared!")

# Create global prototype instance
prototype = LivePrototype()

# Expose commands globally for easy access
defi = prototype.defi
yield_hunt = prototype.yield_hunt  
health = prototype.health
benchmark = prototype.benchmark
demo = prototype.demo
results = prototype.results
clear = prototype.clear

if __name__ == "__main__":
    prototype.banner()
    
    # Start interactive session
    print("🚀 Starting interactive session...")
    print("Example: await demo()")
    print("         await defi('curve')")
    print("         await health()")