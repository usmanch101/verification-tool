#!/usr/bin/env python3

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import requests
from typing import Dict, List, Any
import argparse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

class VerificationResult:
    def __init__(self, component: str, status: str, details: str, evidence_file: str = None):
        self.component = component
        self.status = status
        self.details = details
        self.evidence_file = evidence_file
        self.timestamp = datetime.now().isoformat()

class VerificationTool:
    def __init__(self, config_file: str = "verification_config.json"):
        self.config = self.load_config(config_file)
        self.results = []
        self.evidence_dir = Path("verification_evidence")
        self.evidence_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.evidence_dir / "verification.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self, config_file: str) -> Dict[str, Any]:
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
        api_base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
        database_path = os.getenv('DATABASE_PATH', 'phase2.db')
        
        default_config = {
            "telegram_token": telegram_token,
            "project_name": "AI Project Phase 2",
            "phase2_outputs": {
                "file_structure": {
                    "required_files": ["main.py", "requirements.txt", "config.json", "verification_tool.py"],
                    "required_dirs": ["src/", "tests/", "data/", "verification_evidence/"]
                },
                "database_schema": {
                    "connection_string": f"sqlite:///{database_path}",
                    "required_tables": ["users", "conversations", "models"]
                },
                "api_endpoints": {
                    "base_url": api_base_url,
                    "endpoints": ["/health", "/api/v1/chat", "/api/v1/models"]
                }
            }
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"Created default config file: {config_file}")
            return default_config

    def check_file_structure(self) -> VerificationResult:
        self.logger.info("Checking file structure...")
        
        config = self.config["phase2_outputs"]["file_structure"]
        missing_files = []
        missing_dirs = []
        existing_files = []
        existing_dirs = []
        
        for file_path in config["required_files"]:
            if os.path.exists(file_path):
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        for dir_path in config["required_dirs"]:
            if os.path.exists(dir_path):
                existing_dirs.append(dir_path)
            else:
                missing_dirs.append(dir_path)
        
        evidence = {
            "timestamp": datetime.now().isoformat(),
            "check_type": "file_structure",
            "checked_files": config["required_files"],
            "checked_dirs": config["required_dirs"],
            "existing_files": existing_files,
            "existing_dirs": existing_dirs,
            "missing_files": missing_files,
            "missing_dirs": missing_dirs,
            "current_directory_contents": os.listdir("."),
            "total_files_checked": len(config["required_files"]),
            "total_dirs_checked": len(config["required_dirs"]),
            "files_found": len(existing_files),
            "dirs_found": len(existing_dirs)
        }
        
        evidence_file = self.evidence_dir / f"file_structure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(evidence_file, 'w') as f:
            json.dump(evidence, f, indent=2)
        
        if missing_files or missing_dirs:
            status = "FAIL"
            details = f"Missing {len(missing_files)} files and {len(missing_dirs)} directories"
        else:
            status = "PASS"
            details = f"All {len(existing_files)} files and {len(existing_dirs)} directories found"
        
        return VerificationResult("File Structure", status, details, str(evidence_file))

    def check_database_schema(self) -> VerificationResult:
        self.logger.info("Checking database schema...")
        
        try:
            import sqlite3
            config = self.config["phase2_outputs"]["database_schema"]
            
            db_file = config["connection_string"].replace("sqlite:///", "")
            
            if not os.path.exists(db_file):
                return VerificationResult("Database Schema", "FAIL", f"Database file {db_file} not found", None)
            
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            table_schemas = {}
            for table in existing_tables:
                cursor.execute(f"PRAGMA table_info({table});")
                table_schemas[table] = cursor.fetchall()
            
            missing_tables = []
            for required_table in config["required_tables"]:
                if required_table not in existing_tables:
                    missing_tables.append(required_table)
            
            evidence = {
                "timestamp": datetime.now().isoformat(),
                "check_type": "database_schema",
                "database_file": db_file,
                "database_size_bytes": os.path.getsize(db_file),
                "required_tables": config["required_tables"],
                "existing_tables": existing_tables,
                "missing_tables": missing_tables,
                "table_schemas": table_schemas,
                "total_tables_required": len(config["required_tables"]),
                "total_tables_found": len(existing_tables)
            }
            
            evidence_file = self.evidence_dir / f"database_schema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(evidence_file, 'w') as f:
                json.dump(evidence, f, indent=2)
            
            conn.close()
            
            if missing_tables:
                status = "FAIL"
                details = f"Missing {len(missing_tables)} required tables: {missing_tables}"
            else:
                status = "PASS"
                details = f"All {len(existing_tables)} required tables found"
                
            return VerificationResult("Database Schema", status, details, str(evidence_file))
            
        except Exception as e:
            error_evidence = {
                "timestamp": datetime.now().isoformat(),
                "check_type": "database_schema",
                "error": str(e),
                "error_type": type(e).__name__
            }
            evidence_file = self.evidence_dir / f"database_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(evidence_file, 'w') as f:
                json.dump(error_evidence, f, indent=2)
            return VerificationResult("Database Schema", "FAIL", f"Error checking database: {str(e)}", str(evidence_file))

    def check_api_endpoints(self) -> VerificationResult:
        self.logger.info("Checking API endpoints...")
        
        config = self.config["phase2_outputs"]["api_endpoints"]
        base_url = config["base_url"]
        endpoints = config["endpoints"]
        
        results = {}
        failed_endpoints = []
        successful_endpoints = []
        
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            try:
                response = requests.get(url, timeout=10)
                results[endpoint] = {
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "accessible": response.status_code < 500,
                    "content_length": len(response.content),
                    "headers": dict(response.headers)
                }
                
                if response.status_code < 500:
                    successful_endpoints.append(endpoint)
                else:
                    failed_endpoints.append(endpoint)
                    
            except requests.exceptions.RequestException as e:
                results[endpoint] = {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "accessible": False
                }
                failed_endpoints.append(endpoint)
        
        evidence = {
            "timestamp": datetime.now().isoformat(),
            "check_type": "api_endpoints",
            "base_url": base_url,
            "tested_endpoints": endpoints,
            "results": results,
            "successful_endpoints": successful_endpoints,
            "failed_endpoints": failed_endpoints,
            "total_endpoints_tested": len(endpoints),
            "successful_count": len(successful_endpoints),
            "failed_count": len(failed_endpoints)
        }
        
        evidence_file = self.evidence_dir / f"api_endpoints_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(evidence_file, 'w') as f:
            json.dump(evidence, f, indent=2)
        
        if failed_endpoints:
            status = "FAIL"
            details = f"{len(failed_endpoints)} endpoints failed: {failed_endpoints}"
        else:
            status = "PASS"
            details = f"All {len(successful_endpoints)} endpoints accessible"
        
        return VerificationResult("API Endpoints", status, details, str(evidence_file))

    def run_verification(self, phase: str = "phase2") -> List[VerificationResult]:
        self.logger.info(f"Starting verification for {phase}")
        self.results = []
        
        self.results.append(self.check_file_structure())
        self.results.append(self.check_database_schema())
        self.results.append(self.check_api_endpoints())
        
        return self.results

    def generate_report(self) -> str:
        report = []
        report.append("=" * 60)
        report.append("VERIFICATION REPORT")
        report.append("=" * 60)
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append(f"Project: {self.config.get('project_name', 'AI Project')}")
        report.append("")
        
        all_passed = True
        total_checks = len(self.results)
        passed_checks = 0
        
        for result in self.results:
            status_icon = "PASS" if result.status == "PASS" else "FAIL"
            report.append(f"{status_icon} {result.component}: {result.status}")
            report.append(f"   Details: {result.details}")
            if result.evidence_file:
                report.append(f"   Evidence: {result.evidence_file}")
            report.append("")
            
            if result.status == "PASS":
                passed_checks += 1
            else:
                all_passed = False
        
        report.append("=" * 60)
        report.append(f"SUMMARY: {passed_checks}/{total_checks} checks passed")
        overall_status = "PASS" if all_passed else "FAIL"
        report.append(f"OVERALL STATUS: {overall_status}")
        report.append("=" * 60)
        
        report_file = self.evidence_dir / f"verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(report))
        
        return "\n".join(report)

    async def handle_telegram_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message.text.lower()
        
        if "run phase 2 test" in message or "run verification" in message:
            await update.message.reply_text("Starting Phase 2 verification...")
            
            results = self.run_verification("phase2")
            report = self.generate_report()
            
            await update.message.reply_text(f"```\n{report}\n```", parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "Available commands:\n"
                "'Run Phase 2 test' - Execute verification\n"
                "'Run verification' - Execute verification"
            )

    def start_telegram_bot(self):
        if not TELEGRAM_AVAILABLE:
            print("Telegram library not available")
            return
            
        token = self.config["telegram_token"]
        if token == "YOUR_BOT_TOKEN_HERE":
            print("Please configure your Telegram bot token")
            return
        
        application = Application.builder().token(token).build()
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_telegram_command))
        
        print("Telegram bot started. Send 'Run Phase 2 test' to execute verification.")
        application.run_polling()

def main():
    parser = argparse.ArgumentParser(description="Verification Tool for AI Project")
    parser.add_argument("--mode", choices=["cli", "telegram"], default="cli", 
                      help="Run mode: cli for command line, telegram for bot")
    parser.add_argument("--phase", default="phase2", help="Phase to verify")
    parser.add_argument("--config", default="verification_config.json", help="Config file path")
    
    args = parser.parse_args()
    
    print("Starting Verification Tool...")
    tool = VerificationTool(args.config)
    
    if args.mode == "cli":
        print("Running verification checks...")
        results = tool.run_verification(args.phase)
        report = tool.generate_report()
        print(report)
    else:
        tool.start_telegram_bot()

if __name__ == "__main__":
    main()