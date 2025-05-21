# 变量定义
BUILD_DIR = build
OBFUSCATED_DIR = dist
SRC_DIR = src
NODE_MODULES = node_modules
TSC = ./node_modules/.bin/tsc

# 默认目标
.PHONY: all
all: clean build obfuscate package

# 清理构建目录
.PHONY: clean
clean:
	rm -rf $(BUILD_DIR) $(OBFUSCATED_DIR)

# 检查依赖
.PHONY: check-deps
check-deps:
	@if [ ! -f "$(TSC)" ]; then \
		echo "TypeScript compiler not found. Installing dependencies..."; \
		npm install; \
	fi

# 安装依赖
.PHONY: install
install: check-deps
	npm install
	npm install -g javascript-obfuscator

# 构建项目
.PHONY: build
build: install
	$(TSC) -p tsconfig.json --outDir $(BUILD_DIR)

# 混淆代码
.PHONY: obfuscate
obfuscate: build
	mkdir -p $(OBFUSCATED_DIR)
	javascript-obfuscator $(BUILD_DIR) \
		--output $(OBFUSCATED_DIR) \
		--config obfuscator.config.json

# 打包混淆后的项目
.PHONY: package
package: obfuscate
	cp package.json $(OBFUSCATED_DIR)/
	cp tsconfig.json $(OBFUSCATED_DIR)/
	cp -r $(NODE_MODULES) $(OBFUSCATED_DIR)/
	cd $(OBFUSCATED_DIR) && \
	sed -i '' 's/"start": "ts-node src\/app.ts"/"start": "node app.js"/' package.json && \
	sed -i '' 's/"dev": "ts-node-dev --respawn src\/app.ts"/"dev": "node app.js"/' package.json

# 运行混淆后的项目
.PHONY: run
run: package
	cd $(OBFUSCATED_DIR) && npm start

# 帮助信息
.PHONY: help
help:
	@echo "可用的命令："
	@echo "  make install    - 安装项目依赖"
	@echo "  make build      - 构建项目"
	@echo "  make obfuscate  - 混淆代码"
	@echo "  make package    - 打包混淆后的项目"
	@echo "  make run        - 运行混淆后的项目"
	@echo "  make clean      - 清理构建目录"
	@echo "  make all        - 执行完整的构建流程" 