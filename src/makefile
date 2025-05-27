# Diretórios
BUILD_DIR := ../build
CACHE_DIR := ../cache
DATA_DIR  := ../data

# Arquivos fonte
FORTRAN_SRC := fortran.f90
WRAPPER_SRC := wrapper.c

# Arquivos intermediários (removidos FORTRAN_BC e WRAPPER_BC)
FORTRAN_OBJ := $(BUILD_DIR)/fortran.o
WRAPPER_OBJ := $(BUILD_DIR)/wrapper.o

# Arquivos de saída
OUTPUT_JS := $(BUILD_DIR)/fortran.js
OUTPUT_WASM := $(BUILD_DIR)/fortran.wasm

# Funções exportadas
EXPORTED_FUNCTIONS := '["_get_fixed_integer_wrapper","_start","_malloc","_free"]'
EXPORTED_RUNTIME := '["ccall","cwrap"]'

# Flags de compilação (mudança de flang-new para flang)
FLANG := /opt/flang/host/bin/flang
EMCC := emcc
EMCC_FLAGS := -sWASM=1 -sALLOW_MEMORY_GROWTH=1 -sSINGLE_FILE=0 \
              -sEXPORTED_FUNCTIONS=$(EXPORTED_FUNCTIONS) \
              -sEXPORTED_RUNTIME_METHODS=$(EXPORTED_RUNTIME) \
              -sMODULARIZE=1 -sEXPORT_NAME='FortranModule' \
              -sNO_EXIT_RUNTIME=1 -sINVOKE_RUN=0 \
              -sFORCE_FILESYSTEM=1 \
              --preload-file $(DATA_DIR)@/data \
              --cache $(CACHE_DIR)

.PHONY: all clean

# Regra principal agora depende do HTML também
all: $(OUTPUT_JS) $(BUILD_DIR)/index.html

# Criar diretório build se não existir
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Copiar HTML para build (regra separada para melhor visibilidade)
$(BUILD_DIR)/index.html: index.html | $(BUILD_DIR)
	cp -f $< $@

# Compilar Fortran para objeto WebAssembly DIRETAMENTE (sem bitcode intermediário)
$(FORTRAN_OBJ): $(FORTRAN_SRC) | $(BUILD_DIR)
	$(FLANG) -c $< -o $@

# Compilar wrapper C para objeto WebAssembly DIRETAMENTE (sem bitcode intermediário)
$(WRAPPER_OBJ): $(WRAPPER_SRC) | $(BUILD_DIR)
	$(EMCC) -c $< -o $@

# Link final para JS/WASM
$(OUTPUT_JS): $(FORTRAN_OBJ) $(WRAPPER_OBJ)
	$(EMCC) $^ -L/opt/flang/wasm/lib -lFortranRuntime -o $@ $(EMCC_FLAGS)

clean:
	rm -f "$(BUILD_DIR)/fortran.o" "$(BUILD_DIR)/wrapper.o" \
          "$(BUILD_DIR)/fortran.js" "$(BUILD_DIR)/fortran.wasm" \
          "$(BUILD_DIR)/index.html" \
          $(BUILD_DIR)/*.mod