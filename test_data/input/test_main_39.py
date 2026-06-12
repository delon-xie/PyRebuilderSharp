# Source Generated with Decompyle++
# File: test_main.39.pyc (Python 3.9)

'''
TradingAgents-CN v1.0.0-preview FastAPI Backend
主应用程序入口

Copyright (c) 2025 hsliuping. All rights reserved.
版权所有 (c) 2025 hsliuping。保留所有权利。

This software is proprietary and confidential. Unauthorized copying, distribution,
or use of this software, via any medium, is strictly prohibited.
本软件为专有和机密软件。严禁通过任何媒介未经授权复制、分发或使用本软件。

For commercial licensing, please contact: hsliup@163.com
商业许可咨询，请联系：hsliup@163.com
'''
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import time
from datetime import datetime
from contextlib import asynccontextmanager
import asyncio
from pathlib import Path
from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.logging_config import setup_logging
from app.routers import auth_db as auth, analysis, screening, queue, sse, health, favorites, config, reports, database, operation_logs, tags, tushare_init, akshare_init, baostock_init, historical_data, multi_period_sync, financial_data, news_data, social_media, internal_messages, usage_statistics, model_capabilities, cache, logs, mcp_switch, hermes, hermes_tools
from app.routers import sync as sync_router, multi_source_sync
from app.routers import stocks as stocks_router
from app.routers import stock_data as stock_data_router
from app.routers import stock_sync as stock_sync_router
from app.routers import multi_market_stocks as multi_market_stocks_router
from app.routers import notifications as notifications_router
from app.routers import websocket_notifications as websocket_notifications_router
from app.routers import scheduler as scheduler_router
from app.services.basics_sync_service import get_basics_sync_service
from app.services.multi_source_basics_sync_service import MultiSourceBasicsSyncService
from app.services.scheduler_service import set_scheduler_instance
from app.worker.tushare_sync_service import run_tushare_basic_info_sync, run_tushare_quotes_sync, run_tushare_historical_sync, run_tushare_financial_sync, run_tushare_status_check
from app.worker.akshare_sync_service import run_akshare_basic_info_sync, run_akshare_quotes_sync, run_akshare_historical_sync, run_akshare_financial_sync, run_akshare_status_check
from app.worker.baostock_sync_service import run_baostock_basic_info_sync, run_baostock_daily_quotes_sync, run_baostock_historical_sync, run_baostock_status_check
from app.middleware.operation_log_middleware import OperationLogMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from app.services.quotes_ingestion_service import QuotesIngestionService
from app.routers import paper as paper_router

def get_version():
    '''从 VERSION 文件读取版本号'''
    
    try:
        version_file = Path(__file__).parent.parent / 'VERSION'
        if version_file.exists():
            pass
    return None
    except Exception:
        pass

    return '1.0.0'


async def _print_config_summary(logger):
    '''显示配置摘要'''
    
    try:
        logger.info('======================================================================')
        logger.info('📋 TradingAgents-CN Configuration Summary')
        logger.info('======================================================================')
        import os
        Path = Path
        import pathlib
        current_dir = Path.cwd()
        logger.info(f'''📁 Current working directory: {current_dir}''')
        env_files_to_check = [
            current_dir / '.env',
            current_dir / 'app' / '.env',
            Path(__file__).parent.parent / '.env']
        logger.info('🔍 Checking .env file locations:')
        env_file_found = False
        for env_file in env_files_to_check:
            if env_file.exists():
                logger.info(f'''  ✅ Found: {env_file} (size: {env_file.stat().st_size} bytes)''')
                env_file_found = True
                
                try:
                    with open(env_file, 'r', 'utf-8', **('encoding',)) as f:
                        lines = f.readlines()[:5]
                        logger.info('     Preview (first 5 lines):')
                        for None in enumerate(lines, 1):
                            (i, line) = None
                            if None((lambda .0 = None: (keyword in line.upper() for keyword in .0))(('PASSWORD', 'SECRET', 'KEY', 'TOKEN'))):
                                logger.info(f'''       {i}: {line.split('=')[0]}=***''')
                                continue
                        None(None, None, None)
                    with None:
                        if not None:
                            pass
                except Exception as e:
                    
                    try:
                        logger.warning(f'''     Could not preview file: {e}''')
                    finally:
                        pass
                    continue
                    continue
                    if not env_file_found:
                        logger.warning('⚠️  No .env file found in checked locations')


        logger.info('⚙️  Pydantic Settings Configuration:')
        logger.info(f'''  • Settings class: {settings.__class__.__name__}''')
        logger.info(f'''  • Config source: {getattr(settings.model_config, 'env_file', 'Not specified')}''')
        logger.info(f'''  • Encoding: {getattr(settings.model_config, 'env_file_encoding', 'Not specified')}''')
        key_settings = [
            'HOST',
            'PORT',
            'DEBUG',
            'MONGODB_HOST',
            'REDIS_HOST']
        logger.info('  • Key settings sources:')
        for setting_name in key_settings:
            env_var_name = setting_name
            env_value = os.getenv(env_var_name)
            config_value = getattr(settings, setting_name, None)
            if env_value is not None:
                logger.info(f'''    - {setting_name}: from environment variable ({config_value})''')
            else:
                logger.info(f'''    - {setting_name}: using default value ({config_value})''')
        env = 'Production' if settings.is_production else 'Development'
        logger.info(f'''Environment: {env}''')
        logger.info(f'''MongoDB: {settings.MONGODB_HOST}:{settings.MONGODB_PORT}/{settings.MONGODB_DATABASE}''')
        logger.info(f'''Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}''')
        import os
        if settings.HTTP_PROXY or settings.HTTPS_PROXY:
            logger.info('Proxy Configuration:')
            if settings.HTTP_PROXY:
                logger.info(f'''  HTTP_PROXY: {settings.HTTP_PROXY}''')
            if settings.HTTPS_PROXY:
                logger.info(f'''  HTTPS_PROXY: {settings.HTTPS_PROXY}''')
            if settings.NO_PROXY:
                no_proxy_list = settings.NO_PROXY.split(',')
                if len(no_proxy_list) <= 3:
                    logger.info(f'''  NO_PROXY: {settings.NO_PROXY}''')
                else:
                    logger.info(f'''  NO_PROXY: {','.join(no_proxy_list[:3])}... ({len(no_proxy_list)} domains)''')
            logger.info('  ✅ Proxy environment variables set successfully')
        else:
            logger.info('Proxy: Not configured (direct connection)')
        
        try:
            config_service = config_service
            import app.services.config_service
            await config_service.get_system_config()
            config = await config_service.get_system_config()
            if config and config.llm_configs:
                enabled_llms = (lambda .0: [llm for llm in .0 if llm.enabled])(config.llm_configs)
                logger.info(f'''Enabled LLMs: {len(enabled_llms)}''')
                if enabled_llms:
                    for llm in enabled_llms[:3]:
                        logger.info(f'''  • {llm.provider}: {llm.model_name}''')
                    if len(enabled_llms) > 3:
                        logger.info(f'''  • ... and {len(enabled_llms) - 3} more''')
                    else:
                        logger.warning('⚠️  No LLM enabled. Please configure at least one LLM in Web UI.')
                else:
                    logger.warning('⚠️  No LLM configured. Please configure at least one LLM in Web UI.')
            else:
                except Exception as e:
                    
                    try:
                        logger.warning(f'''⚠️  Failed to check LLM configs: {e}''')
                    finally:
                        pass
                    
                    try:
                        if config and config.data_source_configs:
                            enabled_sources = (lambda .0: [ds for ds in .0 if ds.enabled])(config.data_source_configs)
                            logger.info(f'''Enabled Data Sources: {len(enabled_sources)}''')
                        logger.info('======================================================================')
                    except Exception:
                        
                        try:
                            logger.error(f'''Failed to print config summary: {e}''')
                        finally:
                            pass
                        return None







def lifespan(app = None):
    '''应用生命周期管理'''
    setup_logging()
    logger = logging.getLogger('app.main')
    await init_db()
    
    try:
        bridge_config_to_env = bridge_config_to_env
        import app.core.config_bridge
        bridge_config_to_env()
    except Exception:
        
        try:
            logger.warning(f'''⚠️  配置桥接失败: {e}''')
            logger.warning('⚠️  TradingAgents 将使用 .env 文件中的配置')
        finally:
            pass
        await _print_config_summary(logger)
        logger.info('TradingAgents FastAPI backend started')
        if settings.QUOTES_BACKFILL_ON_STARTUP:
            pass


    scheduler = None
    
    try:
        croniter = croniter
        import croniter
    except Exception as croniter:
        pass

    
    try:
        yield None
    if scheduler:
        pass

    await close_db()
    logger.info('TradingAgents FastAPI backend stopped')

lifespan = None(lifespan)
app = FastAPI('TradingAgents-CN API', '股票分析与批量队列系统 API', get_version(), '/docs' if settings.DEBUG else None, '/redoc' if settings.DEBUG else None, lifespan, **('title', 'description', 'version', 'docs_url', 'redoc_url', 'lifespan'))
if not settings.DEBUG:
    app.add_middleware(TrustedHostMiddleware, settings.ALLOWED_HOSTS, **('allowed_hosts',))
app.add_middleware(CORSMiddleware, settings.ALLOWED_ORIGINS, True, [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS'], [
    '*'], **('allow_origins', 'allow_credentials', 'allow_methods', 'allow_headers'))
app.add_middleware(OperationLogMiddleware)

async def log_requests(request = None, call_next = None):
    start_time = time.time()
    if request.url.path in ('/health', '/favicon.ico') or request.url.path.startswith('/static'):
        await call_next(request)
        response = await call_next(request)
        return response
    logger = None.getLogger('webapi')
    logger.info(f'''🔄 {request.method} {request.url.path} - 开始处理''')
    await call_next(request)
    response = await call_next(request)
    process_time = time.time() - start_time
    status_emoji = '✅' if response.status_code < 400 else '❌'
    logger.info(f'''{status_emoji} {request.method} {request.url.path} - 状态: {response.status_code} - 耗时: {process_time:.3f}s''')
    return response

log_requests = None(log_requests)
from app.middleware.request_id import RequestIDMiddleware
app.add_middleware(RequestIDMiddleware)

async def global_exception_handler(request = None, exc = None):
    logging.error(f'''Unhandled exception: {exc}''', True, **('exc_info',))
    return JSONResponse(500, {
        'error': {
            'code': 'INTERNAL_SERVER_ERROR',
            'message': 'Internal server error occurred',
            'request_id': getattr(request.state, 'request_id', None) } }, **('status_code', 'content'))

global_exception_handler = None(global_exception_handler)

async def test_log():
    '''测试日志中间件是否工作'''
    print('🧪 测试端点被调用 - 这条消息应该出现在控制台')
    return {
        'message': '测试成功',
        'timestamp': time.time() }

test_log = app.get('/api/test-log')(test_log)
app.include_router(health.router, '/api', [
    'health'], **('prefix', 'tags'))
app.include_router(auth.router, '/api/auth', [
    'authentication'], **('prefix', 'tags'))
app.include_router(analysis.router, '/api/analysis', [
    'analysis'], **('prefix', 'tags'))
app.include_router(reports.router, [
    'reports'], **('tags',))
app.include_router(screening.router, '/api/screening', [
    'screening'], **('prefix', 'tags'))
app.include_router(queue.router, '/api/queue', [
    'queue'], **('prefix', 'tags'))
app.include_router(favorites.router, '/api', [
    'favorites'], **('prefix', 'tags'))
app.include_router(stocks_router.router, '/api', [
    'stocks'], **('prefix', 'tags'))
app.include_router(multi_market_stocks_router.router, '/api', [
    'multi-market'], **('prefix', 'tags'))
app.include_router(stock_data_router.router, [
    'stock-data'], **('tags',))
app.include_router(stock_sync_router.router, [
    'stock-sync'], **('tags',))
app.include_router(tags.router, '/api', [
    'tags'], **('prefix', 'tags'))
app.include_router(config.router, '/api', [
    'config'], **('prefix', 'tags'))
app.include_router(model_capabilities.router, [
    'model-capabilities'], **('tags',))
app.include_router(usage_statistics.router, [
    'usage-statistics'], **('tags',))
app.include_router(database.router, '/api/system', [
    'database'], **('prefix', 'tags'))
app.include_router(cache.router, [
    'cache'], **('tags',))
app.include_router(operation_logs.router, '/api/system', [
    'operation_logs'], **('prefix', 'tags'))
app.include_router(logs.router, '/api/system', [
    'logs'], **('prefix', 'tags'))
from app.routers import system_config as system_config_router
app.include_router(system_config_router.router, '/api/system', [
    'system'], **('prefix', 'tags'))
app.include_router(notifications_router.router, '/api', [
    'notifications'], **('prefix', 'tags'))
app.include_router(websocket_notifications_router.router, '/api', [
    'websocket'], **('prefix', 'tags'))
app.include_router(scheduler_router.router, [
    'scheduler'], **('tags',))
app.include_router(mcp_switch.router, '/api', [
    'mcp-switch'], **('prefix', 'tags'))
app.include_router(hermes.router, '/api', [
    'hermes'], **('prefix', 'tags'))
app.include_router(hermes_tools.router, '/api', [
    'hermes-tools'], **('prefix', 'tags'))
app.include_router(sse.router, '/api/stream', [
    'streaming'], **('prefix', 'tags'))
app.include_router(sync_router.router)
app.include_router(multi_source_sync.router)
app.include_router(paper_router.router, '/api', [
    'paper'], **('prefix', 'tags'))
app.include_router(tushare_init.router, '/api', [
    'tushare-init'], **('prefix', 'tags'))
app.include_router(akshare_init.router, '/api', [
    'akshare-init'], **('prefix', 'tags'))
app.include_router(baostock_init.router, '/api', [
    'baostock-init'], **('prefix', 'tags'))
app.include_router(historical_data.router, [
    'historical-data'], **('tags',))
app.include_router(multi_period_sync.router, [
    'multi-period-sync'], **('tags',))
app.include_router(financial_data.router, [
    'financial-data'], **('tags',))
app.include_router(news_data.router, [
    'news-data'], **('tags',))
app.include_router(social_media.router, [
    'social-media'], **('tags',))
app.include_router(internal_messages.router, [
    'internal-messages'], **('tags',))

async def root():
    '''根路径，返回API信息'''
    print('🏠 根路径被访问')
    return {
        'name': 'TradingAgents-CN API',
        'version': get_version(),
        'status': 'running',
        'docs_url': '/docs' if settings.DEBUG else None }

root = app.get('/')(root)
if __name__ == '__main__':
    uvicorn.run('app.main:app', settings.HOST, settings.PORT, settings.DEBUG, 'info', [
        'app'] if settings.DEBUG else None, [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.git',
        '.pytest_cache',
        '*.log',
        '*.tmp'] if settings.DEBUG else None, [
        '*.py'] if settings.DEBUG else None, **('host', 'port', 'reload', 'log_level', 'reload_dirs', 'reload_excludes', 'reload_includes'))
