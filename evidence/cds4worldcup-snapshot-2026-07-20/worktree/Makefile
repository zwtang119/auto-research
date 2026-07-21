.PHONY: help audit verify lint check clean init results

help: ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

audit: ## 审计知识库
	python3 scripts/audit.py --root wiki/
	python3 scripts/audit.py --root example/

verify: ## 验证知识库
	python3 scripts/verify.py --root wiki/
	python3 scripts/verify.py --root example/

lint: ## Markdown 语法检查
	@echo "Markdown lint (install: npm i -g markdownlint-cli)"
	markdownlint '**/*.md' --ignore node_modules --ignore docs/references --config .markdownlint.json || true

check: audit verify ## 完整检查（审计 + 验证）
	@echo "✅ All checks passed"

clean: ## 清理临时文件
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf _publish _site 2>/dev/null || true

init: ## 初始化知识库
	python3 scripts/init.py --root .

results: ## 发布最新结果到站点
	@echo "Building site with latest results..."
	python3 scripts/build_site_data.py
	@rm -rf _publish
	@mkdir -p _publish
	@touch _publish/.nojekyll
	@cp -r site/* _publish/
	@rm -f _publish/_config.yml
	@echo "✅ Public site prepared in _publish"
