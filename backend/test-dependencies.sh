#!/bin/bash

# Script de teste para verificar dependências
echo "🧪 Testando dependências do sistema..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Detectar sistema operacional
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo 'macos';;
        Linux*)     echo 'linux';;
        CYGWIN*|MINGW32*|MSYS*|MINGW*) echo 'windows';;
        *)          echo 'unknown';;
    esac
}

OS=$(detect_os)
print_info "Sistema operacional detectado: $OS"

# Testar jq
echo ""
print_info "Testando jq..."
if command -v jq &> /dev/null; then
    print_success "jq está instalado: $(which jq)"
    echo '{"test": "success"}' | jq '.' > /dev/null && print_success "jq está funcionando"
else
    print_error "jq não está instalado"
fi

# Testar qrencode
echo ""
print_info "Testando qrencode..."
if command -v qrencode &> /dev/null; then
    print_success "qrencode está instalado: $(which qrencode)"
    echo "test" | qrencode -t ANSIUTF8 | head -5 > /dev/null && print_success "qrencode está funcionando"
else
    print_error "qrencode não está instalado"
fi

# Testar Docker
echo ""
print_info "Testando Docker..."
if command -v docker &> /dev/null; then
    print_success "Docker está instalado: $(which docker)"
    docker --version
else
    print_error "Docker não está instalado"
fi

# Testar Docker Compose
echo ""
print_info "Testando Docker Compose..."
if command -v docker-compose &> /dev/null; then
    print_success "Docker Compose está instalado: $(which docker-compose)"
    docker-compose --version
else
    print_error "Docker Compose não está instalado"
fi

# Testar curl
echo ""
print_info "Testando curl..."
if command -v curl &> /dev/null; then
    print_success "curl está instalado: $(which curl)"
    curl --version | head -1
else
    print_error "curl não está instalado"
fi

echo ""
print_info "Teste concluído!" 