# ============================================================================
# install.ps1 — Despliega el kit de Claude Code a un proyecto Python
# ============================================================================
# Uso (PowerShell):
#   .\install.ps1 -TargetDir C:\ruta\a\tu\proyecto -PackageName mi_paquete `
#       [-ProjectName mi-paquete] `
#       [-AuthorName "Ada Lovelace"] [-AuthorEmail ada@example.com] `
#       [-GithubUser ada] [-NoPrompt]
#
# Si el proyecto no existe, se crea. Si existe, se añaden los ficheros sin
# pisar lo que ya tengas (los conflictos se reportan).
#
# Si AuthorName/AuthorEmail/GithubUser no se pasan, se preguntan
# interactivamente. Con -NoPrompt se usan defaults sin preguntar.
# ============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetDir,

    [Parameter(Mandatory=$true)]
    [string]$PackageName,

    [string]$ProjectName = "",
    [string]$AuthorName = "",
    [string]$AuthorEmail = "",
    [string]$GithubUser = "",
    [switch]$NoPrompt
)

if (-not $ProjectName) {
    $ProjectName = $PackageName -replace '_', '-'
}

function Read-WithDefault {
    param([string]$Prompt, [string]$Default)
    if ($NoPrompt -or [Console]::IsInputRedirected) { return $Default }
    $answer = Read-Host "$Prompt [$Default]"
    if ([string]::IsNullOrWhiteSpace($answer)) { return $Default }
    return $answer
}

if (-not $AuthorName)  { $AuthorName  = Read-WithDefault "Autor (nombre)"     "Tu Nombre" }
if (-not $AuthorEmail) { $AuthorEmail = Read-WithDefault "Autor (email)"      "tu@email.com" }
if (-not $GithubUser)  { $GithubUser  = Read-WithDefault "Usuario de GitHub"  "usuario" }

$ErrorActionPreference = "Stop"
$KitDir = $PSScriptRoot

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host " Despliegue del kit Claude Code para Python" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Origen (kit):  $KitDir"
Write-Host "Destino:       $TargetDir"
Write-Host "Paquete:       $PackageName  (nombre Python con underscores)"
Write-Host "Proyecto:      $ProjectName  (nombre PyPI con guiones)"
Write-Host "Autor:         $AuthorName <$AuthorEmail>"
Write-Host "GitHub user:   $GithubUser"
Write-Host ""

# Crear destino si no existe
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
    Write-Host "✓ Carpeta destino creada" -ForegroundColor Green
}

# Lista de ficheros/carpetas ÚTILES a copiar
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

# settings.local.json es per-developer: nunca debe llegar al destino.
$LocalSettings = Join-Path $TargetDir ".claude\settings.local.json"
if (Test-Path $LocalSettings) { Remove-Item -Path $LocalSettings -Force }

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

# Sustituir tokens en los ficheros copiados
Write-Host ""
Write-Host "Personalizando nombres y metadatos..." -ForegroundColor Yellow
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
        $content = Get-Content $path -Raw
        $content = $content.Replace('mi_paquete',          $PackageName)
        $content = $content.Replace('mi-paquete',          $ProjectName)
        $content = $content.Replace('github.com/usuario/', "github.com/$GithubUser/")
        $content = $content.Replace('Tu Nombre',           $AuthorName)
        $content = $content.Replace('tu@email.com',        $AuthorEmail)
        Set-Content -Path $path -Value $content -Encoding UTF8
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
