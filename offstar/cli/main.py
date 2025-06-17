#!/usr/bin/env python3
# OffStar CLI - Command-line interface for autonomous agent
import click
import asyncio
import json
from datetime import datetime
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from offstar.core.task_processor import AsyncTaskProcessor, TaskPriority
from offstar.plugins.defi_plugin import CustomDeFiPlugin

class OffStarCLI:
    def __init__(self):
        self.processor = None
        self.defi_plugin = None
        
    async def initialize(self):
        """Initialize OffStar system"""
        self.processor = AsyncTaskProcessor(max_concurrent_tasks=5)
        self.defi_plugin = CustomDeFiPlugin()
        
        # Register plugins with processor
        await self.processor.register_plugin('defi', self.defi_plugin)

# Global CLI instance
cli_instance = OffStarCLI()

@click.group()
def cli():
    """OffStar - Autonomous AI Agent CLI"""
    pass

@cli.command()
def status():
    """Show system status"""
    click.echo("🌟 OffStar Autonomous Agent")
    click.echo("Status: Ready for autonomous operation")
    click.echo(f"Timestamp: {datetime.now().isoformat()}")

@cli.command()
@click.option('--protocol', default='uniswap_v3', help='DeFi protocol to analyze')
def analyze_protocol(protocol):
    """Analyze DeFi protocol metrics"""
    async def _analyze():
        await cli_instance.initialize()
        
        # Start processor
        processor_task = asyncio.create_task(cli_instance.processor.start_processing())
        
        # Submit analysis task
        task_id = await cli_instance.processor.submit_task(
            "defi_metrics",
            {'protocol': protocol},
            TaskPriority.HIGH
        )
        
        click.echo(f"⏳ Analyzing {protocol}... (Task ID: {task_id})")
        
        # Wait for completion
        while True:
            status = await cli_instance.processor.get_task_status(task_id)
            if status['status'] in ['completed', 'failed']:
                break
            await asyncio.sleep(0.5)
        
        # Display results
        if status['status'] == 'completed':
            result = status['result']
            click.echo(f"\n📊 {protocol.upper()} Analysis Results:")
            click.echo(f"💰 TVL: ${result['tvl']:,.0f}")
            click.echo(f"📈 24h Volume: ${result['volume_24h']:,.0f}")
            click.echo(f"🎯 APY: {result['apy']:.2%}")
            click.echo(f"⚠️ Risk Score: {result['risk_score']:.1f}/10")
        else:
            click.echo(f"❌ Analysis failed: {status['error']}")
        
        # Stop processor
        await cli_instance.processor.stop_processing()
        processor_task.cancel()
    
    asyncio.run(_analyze())

@cli.command()
def find_yield():
    """Find optimal yield opportunities"""
    async def _find_yield():
        await cli_instance.initialize()
        
        # Start processor
        processor_task = asyncio.create_task(cli_instance.processor.start_processing())
        
        # Submit yield optimization task
        task_id = await cli_instance.processor.submit_task(
            "yield_optimization",
            {},
            TaskPriority.HIGH
        )
        
        click.echo("🔍 Finding optimal yield opportunities...")
        
        # Wait for completion
        while True:
            status = await cli_instance.processor.get_task_status(task_id)
            if status['status'] in ['completed', 'failed']:
                break
            await asyncio.sleep(0.5)
        
        # Display results
        if status['status'] == 'completed':
            opportunities = status['result']['opportunities']
            click.echo("\n🏆 Top Yield Opportunities:")
            
            for i, opp in enumerate(opportunities[:3], 1):
                click.echo(f"\n{i}. {opp['protocol'].upper()}")
                click.echo(f"   APY: {opp['apy']:.2%}")
                click.echo(f"   Risk Score: {opp['risk_score']:.1f}/10")
                click.echo(f"   Risk-Adjusted Yield: {opp['risk_adjusted_yield']:.2%}")
        else:
            click.echo(f"❌ Optimization failed: {status['error']}")
        
        # Stop processor
        await cli_instance.processor.stop_processing()
        processor_task.cancel()
    
    asyncio.run(_find_yield())

@cli.command()
def health():
    """Check system health"""
    async def _health_check():
        await cli_instance.initialize()
        
        # Check plugin health
        health_result = await cli_instance.defi_plugin.monitor_health()
        
        click.echo("🏥 System Health Report:")
        status_icon = "✅" if health_result['status'] == 'healthy' else "❌"
        click.echo(f"{status_icon} DeFi Plugin: {health_result['status']}")
        
        if health_result['status'] != 'healthy' and health_result.get('last_error'):
            click.echo(f"   Error: {health_result['last_error']}")
        
        # System metrics
        if cli_instance.processor:
            metrics = await cli_instance.processor.get_system_metrics()
            click.echo(f"\n📊 System Metrics:")
            click.echo(f"   Active Tasks: {metrics['active_tasks']}")
            click.echo(f"   Queued Tasks: {metrics['queued_tasks']}")
            click.echo(f"   Completed Tasks: {metrics['completed_tasks']}")
            click.echo(f"   Plugins: {metrics['plugins_registered']}")
    
    asyncio.run(_health_check())

@cli.command()
def demo():
    """Run complete OffStar demo"""
    async def _demo():
        click.echo("🚀 OffStar Autonomous Agent Demo")
        click.echo("=" * 40)
        
        await cli_instance.initialize()
        
        # Start processor
        processor_task = asyncio.create_task(cli_instance.processor.start_processing())
        
        # Run multiple analyses
        protocols = ['uniswap_v3', 'aave_v3', 'curve']
        tasks = []
        
        click.echo("📊 Analyzing multiple protocols...")
        
        for protocol in protocols:
            task_id = await cli_instance.processor.submit_task(
                "defi_metrics",
                {'protocol': protocol},
                TaskPriority.HIGH
            )
            tasks.append((protocol, task_id))
        
        # Wait for all completions
        results = []
        for protocol, task_id in tasks:
            while True:
                status = await cli_instance.processor.get_task_status(task_id)
                if status['status'] in ['completed', 'failed']:
                    break
                await asyncio.sleep(0.1)
            
            if status['status'] == 'completed':
                results.append((protocol, status['result']))
        
        # Display comparative results
        click.echo(f"\n📈 Comparative Analysis:")
        for protocol, result in results:
            click.echo(f"\n{protocol.upper()}:")
            click.echo(f"  TVL: ${result['tvl']:,.0f}")
            click.echo(f"  APY: {result['apy']:.2%}")
            click.echo(f"  Risk: {result['risk_score']:.1f}/10")
        
        # Find best opportunities
        click.echo(f"\n🔍 Calculating optimal yields...")
        task_id = await cli_instance.processor.submit_task("yield_optimization", {}, TaskPriority.HIGH)
        
        while True:
            status = await cli_instance.processor.get_task_status(task_id)
            if status['status'] in ['completed', 'failed']:
                break
            await asyncio.sleep(0.1)
        
        if status['status'] == 'completed':
            opportunities = status['result']['opportunities']
            click.echo(f"\n🏆 Top Recommendation: {opportunities[0]['protocol'].upper()}")
            click.echo(f"   Risk-Adjusted Yield: {opportunities[0]['risk_adjusted_yield']:.2%}")
        
        click.echo(f"\n✅ Demo Complete!")
        
        # Stop processor
        await cli_instance.processor.stop_processing()
        processor_task.cancel()
    
    asyncio.run(_demo())

if __name__ == '__main__':
    cli()