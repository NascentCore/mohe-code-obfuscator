# 变量定义
PYTHON := python3
BUILD_DIR := build
DIST_DIR := dist
SRC_DIR := src
REQUIREMENTS := requirements.txt

# 默认目标
all: clean build deploy

# 清理构建文件
clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR)
	find . -name "*.so" -delete
	find . -name "*.c" -delete

# 创建必要的目录
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(DIST_DIR):
	mkdir -p $(DIST_DIR)/src

# 构建 .so 文件
build:
	$(PYTHON) setup.py build_ext --inplace

# 部署到 dist 目录
deploy: $(DIST_DIR)
	@echo "Deploying files to dist directory..."
	# 复制整个 src 目录到 dist
	cp -r $(SRC_DIR)/* $(DIST_DIR)/src/
	# 删除所有 .py 文件（除了需要保留的文件）
	find $(DIST_DIR) -name "*.py" ! -name "app.py" ! -name "__init__.py" ! -name "__main__.py" ! -name "config.py" ! -name "dependencies.py" ! -name "errors.py" ! -name "files.py" ! -name "bases.py" -delete
	# 复制配置文件
	cp .env $(DIST_DIR)/
	cp Dockerfile $(DIST_DIR)/
	cp requirements.txt $(DIST_DIR)/
	cp openapi.yaml $(DIST_DIR)/
	
# 安装依赖
install:
	pip install -r $(REQUIREMENTS)
	pip install cython

.PHONY: all clean build deploy install