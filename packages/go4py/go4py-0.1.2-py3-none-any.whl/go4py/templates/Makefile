.PHONY: clean cpython-extention


# --- Platform-specific ---
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux) # 
    SHARED_LIB_EXT := .so
    LDFLAGS_EXTRA :=
else ifeq ($(UNAME_S),Darwin)
    SHARED_LIB_EXT := .dylib
    LDFLAGS_EXTRA :=
else ifneq (,$(findstring NT,$(OS))) # Windows
    # Assuming Windows with a GCC-compatible compiler (MinGW, MSYS2)
    SHARED_LIB_EXT := .dll
    LDFLAGS_EXTRA := # -Wl,--export-all-symbols # Uncomment if needed with MinGW
else
    $(warning OS is: $(UNAME_S) - assuming Linux)
    SHARED_LIB_EXT := .so
    LDFLAGS_EXTRA :=
endif

ifneq (,$(findstring NT,$(OS))) # Windows
    RM = rmdir /s /q
    MKDIR = mkdir
else
    RM = rm -rf
    MKDIR = mkdir -p
endif


# -- Variables ---
MODULE_NAME := {{ module_name }}
BUILD_DIR := ./artifacts/build
PYTHON_INCLUDE=$(shell python -c "import sysconfig;print(sysconfig.get_path('include'))")
GO_FILES := $(shell find . -name "*.go")


# --- Targets ---
ARTIFACTS_DIR := ./artifacts
PARSER_TARGET := ${ARTIFACTS_DIR}/functions.json
GO_TARGET := ${BUILD_DIR}/lib${MODULE_NAME}.a
FINAL_TARGET := __init__${SHARED_LIB_EXT} # __init__.so


# --- Build Flags ---
CFLAGS := -shared -fPIC -I${PYTHON_INCLUDE}
LDFLAGS := -L${BUILD_DIR} -l${MODULE_NAME} ${LDFLAGS_EXTRA}


# --- Rules ---
all:  ${FINAL_TARGET}

${ARTIFACTS_DIR}:
	@${MKDIR} ${ARTIFACTS_DIR}

# 1. Parsing Go codes
${PARSER_TARGET}: ${GO_FILES} ${ARTIFACTS_DIR}
	@go4py textbox Step-1: "Parsing Go code"
	go4py parse ./src

# 2. Build Go files
${GO_TARGET}: ${PARSER_TARGET}
	@go4py textbox Step-2: "Building Go code"
	go build -buildmode=c-archive -o ${GO_TARGET} ./src

# 3. Generate Python wrapper code
cpython-extention: ${PARSER_TARGET} ${GO_TARGET}
	@go4py textbox Step-3: "Generating CPython wrapper code"
	python -m go4py.code_gen ${MODULE_NAME}

# 4. Build final shared library
${FINAL_TARGET}: cpython-extention
	@go4py textbox Step-4: "Building final shared library"
	gcc ${CFLAGS} -o ${FINAL_TARGET} $(wildcard cpython-extention/*.c) ${LDFLAGS}
	@go4py textbox Done!

# Clean build artifacts
clean:
	$(RM) ${BUILD_DIR} ./*.so
