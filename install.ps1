# ============================================================================
# install.ps1 — Despliega el kit de Claude Code a un proyecto Python
# ============================================================================
# Uso (PowerShell):
#   .\install.ps1 -TargetDir C:\ruta\a\tu\proyecto -PackageName mi_paquete
#
# Si el proyecto no existe, se crea. Si existe, se añaden los ficheros sin
# pisar lo que ya tengas (los conflictos se reportan).
# ============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetDir,

    [Parameter(Mandatory=$true)]
    [string]$PackageName,

    [string]$ProjectName = ""
)

if (-not $ProjectName) {
    $ProjectName = $PackageName -replace '_', '-'
}

$ErrorActionPreference = "Stop"
$KitDir = $PSScriptRoot

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host " Despliegue del kit Claude Code para Python" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Origen (kit): $KitDir"
Write-Host "Destino:      $TargetDir"
Write-Host "Paquete:      $PackageName  (nombre Python con underscores)"
Write-Host "Proyecto:     $ProjectName  (nombre PyPI con guiones)"
Write-Host ""

# Crear destino si no existe
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
    Write-Host "✓ Carpeta destino creada" -ForegroundColor Green
}

# Lista de ficheros/carpetas ÚTILES a copiar (todo lo que NO está obsoleto)
$IncludeItems = @(
    "CLAUDE.md",
    "README.md",
    "GUIA_CLAUDE_CODE.md",
    "pyproject.toml",
    ".gitignore",
    ".python-version",
    ".pre-commit-config.yaml",
    ".mcp.json",
    ".claude",
    "docs"
)

Write-Host ""
Write-Host "Copiando ficheros..." -ForegroundColor Yellow

foreach ($item in $IncludeItems) {
    $src = Join-Path $KitDir $item
    $dst = Join-Path $TargetDir $item

    if (-not (Test-Path $src)) {
        Write-Host "  · $item  (no existe en el kit, salto)" -ForegroundColor DarkGray
        continue
    }

    if (Test-Path $dst) {
        Write-Host "  · $item  ya existe en destino — fusión recursiva" -ForegroundColor DarkYellow
    } else {
        Write-Host "  · $item" -ForegroundColor Green
    }

    Copy-Item -Path $src -Destination $dst -Recurse -Force
}

# Crear estructura src/ y tests/ con el nombre real del paquete
Write-Host ""
Write-Host "Creando estructura del paquete..." -ForegroundColor Yellow
$SrcPkg = Join-Path $TargetDir "src\$PackageName"
$TestsDir = Join-Path $TargetDir "tests"
New-Item -ItemType Directory -Force -Path $SrcPkg | Out-Null
New-Item -ItemType Directory -Force -Path $TestsDir | Out-Null

$InitContent = @"
"""$PackageName paquete."""

__version__ = "0.1.0"
"@
Set-Content -Path (Join-Path $SrcPkg "__init__.py") -Value $InitContent -Encoding UTF8

Set-Content -Path (Join-Path $TestsDir "__init__.py") -Value "" -Encoding UTF8

Write-Host "  · src\$PackageName\__init__.py" -ForegroundColor Green
Write-Host "  · tests\__init__.py" -ForegroundColor Green

# Sustituir 'mi_paquete' y 'mi-paquete' por los nombres reales en los ficheros copiados
Write-Host ""
Write-Host "Personalizando nombres..." -ForegroundColor Yellow
$FilesToCustomize = @(
    "pyproject.toml",
    "CLAUDE.md",
    "README.md",
    "docs\index.md",
    "docs\STATE.md",
    "docs\specs\README.md",
    "docs\specs\_template.md",
    "docs\specs\0001-ejemplo.md"
)

foreach ($f in $FilesToCustomize) {
    $path = Join-Path $TargetDir $f
    if (Test-Path $path) {
        (Get-Content $path -Raw) `
            -replace 'mi_paquete', $PackageName `
            -replace 'mi-paquete', $ProjectName `
            | Set-Content -Path $path -Encoding UTF8
        Write-Host "  · $f" -ForegroundColor Green
    }
}

# Inicializar git si no existe
Write-Host ""
Write-Host "Inicializando git..." -ForegroundColor Yellow
Push-Location $TargetDir
if (-not (Test-Path ".git")) {
    git init | Out-Null
    Write-Host "  · git init OK" -ForegroundColor Green
} else {
    Write-Host "  · ya existe .git, salto" -ForegroundColor DarkGray
}
Pop-Location

# Sync de dependencias
Write-Host ""
Write-Host "Instalando dependencias con uv..." -ForegroundColor Yellow
Push-Location $TargetDir
try {
    uv sync --all-extras --dev
    Write-Host "  · uv sync OK" -ForegroundColor Green
} catch {
    Write-Host "  · uv sync falló. Ejecuta manualmente: uv sync --all-extras --dev" -ForegroundColor Red
}

# Pre-commit
Write-Host ""
Write-Host "Instalando hooks de pre-commit..." -ForegroundColor Yellow
try {
    uv run pre-commit install
    Write-Host "  · pre-commit install OK" -ForegroundColor Green
} catch {
    Write-Host "  · pre-commit install falló. Ejecuta manualmente: uv run pre-commit install" -ForegroundColor Red
}
Pop-Location

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host " ✅ Instalación completa" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Siguientes pasos:"
Write-Host "  1. cd `"$TargetDir`""
Write-Host "  2. claude                    # Lanza Claude Code"
Write-Host "  3. /spec `"primera feature`"  # Crea tu primera spec"
Write-Host ""
Write-Host "Lee docs/index.md y GUIA_CLAUDE_CODE.md para conocer el flujo."
