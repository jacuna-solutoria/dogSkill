# Helpers de git worktree con la convencion T#<num>-<nombre-corto>.
# Uso: dot-source en la sesion ->  . .\scripts\worktree.ps1
# Luego:  New-Worktree -Numero 1234 -Slug "login-con-correo"
#         Get-Worktrees
#         Remove-Worktree -Numero 1234
#         Open-WorktreeConsole -Path ..\miapp-T1234   # abre una consola en la carpeta

function Get-RepoRoot {
    $root = git rev-parse --show-toplevel 2>$null
    if (-not $root) { throw "No estas dentro de un repositorio git." }
    return (Resolve-Path $root).Path
}

function Get-BaseBranch {
    # Resuelve la rama base (main/master) sin asumir.
    $ref = git symbolic-ref refs/remotes/origin/HEAD 2>$null
    if ($ref) { return ($ref -replace '^refs/remotes/origin/', '') }
    return 'main'
}

function Open-WorktreeConsole {
    # Abre una consola NUEVA para el usuario, ya parada en la carpeta del worktree.
    # Asi el agente NO tiene que hacer 'cd' (que le revuelve el contexto): el agente
    # se queda donde estaba y, si necesita tocar el worktree, usa 'git -C <ruta>'.
    # Orden de preferencia exigido: 1) Windows Terminal (wt)  2) PowerShell  3) cmd.
    [CmdletBinding()]
    param([Parameter(Mandatory)][string] $Path)

    if (-not (Test-Path $Path)) { throw "No existe la carpeta: $Path" }
    $full = (Resolve-Path $Path).Path

    # 1) Windows Terminal: ventana nueva (-w -1) con la carpeta como directorio inicial (-d).
    $wt = Get-Command wt -ErrorAction SilentlyContinue
    if ($wt) {
        try {
            Start-Process -FilePath wt -ArgumentList '-w', '-1', '-d', $full -ErrorAction Stop
            Write-Host "Consola abierta en Windows Terminal: $full" -ForegroundColor Green
            return
        } catch {
            Write-Host "Windows Terminal no abrio ($($_.Exception.Message)); pruebo PowerShell." -ForegroundColor Yellow
        }
    }

    # 2) PowerShell: pwsh 7 si existe, si no Windows PowerShell. Start-Process fija el cwd.
    $ps = Get-Command pwsh -ErrorAction SilentlyContinue
    if (-not $ps) { $ps = Get-Command powershell -ErrorAction SilentlyContinue }
    if ($ps) {
        try {
            Start-Process -FilePath $ps.Source -ArgumentList '-NoExit' -WorkingDirectory $full -ErrorAction Stop
            Write-Host "Consola abierta en $($ps.Name): $full" -ForegroundColor Green
            return
        } catch {
            Write-Host "PowerShell no abrio ($($_.Exception.Message)); pruebo cmd." -ForegroundColor Yellow
        }
    }

    # 3) cmd: ultimo recurso. /K mantiene la ventana abierta.
    $cmd = Get-Command cmd -ErrorAction SilentlyContinue
    if ($cmd) {
        try {
            Start-Process -FilePath cmd -ArgumentList '/K' -WorkingDirectory $full -ErrorAction Stop
            Write-Host "Consola abierta en cmd: $full" -ForegroundColor Green
            return
        } catch {
            Write-Host "cmd no abrio ($($_.Exception.Message))." -ForegroundColor Yellow
        }
    }

    Write-Host "No encontre wt, PowerShell ni cmd. Abre una consola a mano en: $full" -ForegroundColor Yellow
}

function New-Worktree {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][int]    $Numero,
        [Parameter(Mandatory)][string] $Slug,
        [string]   $Base,        # base explicita; si se omite, usa origin/<base> tras fetch
        [switch]   $SkipFetch,   # no hacer git fetch antes de crear el worktree
        [switch]   $NoConsole,   # no abrir una consola nueva en la carpeta del worktree
        # Archivos/carpetas ignorados por git que la app necesita para correr y
        # que hay que copiar desde el repo oficial al worktree nuevo.
        # NO incluir .venv ni node_modules: esos se regeneran por carpeta.
        [string[]] $Config = @('.env')
    )
    $root = Get-RepoRoot
    $repoName = Split-Path $root -Leaf

    if (-not $Base) {
        # Nacer desde lo ultimo del remoto: fetch + origin/<base>.
        if (-not $SkipFetch) { git fetch origin | Out-Null }
        $Base = "origin/" + (Get-BaseBranch)
    }

    $branch = "T#$Numero-$Slug"
    $dir    = Join-Path (Split-Path $root -Parent) "$repoName-T$Numero"

    if (Test-Path $dir) { throw "Ya existe la carpeta: $dir" }

    git worktree add $dir -b $branch $Base
    if ($LASTEXITCODE -ne 0) { throw "git worktree add fallo." }

    foreach ($item in $Config) {
        $src = Join-Path $root $item
        if (Test-Path $src) {
            Copy-Item $src (Join-Path $dir $item) -Recurse -Force
            Write-Host "Copiado $item -> $dir" -ForegroundColor Green
        } else {
            Write-Host "No existe '$item' en el repo principal; se omite." -ForegroundColor Yellow
        }
    }

    Write-Host "Worktree listo: $dir  (rama $branch desde $Base)" -ForegroundColor Green
    Write-Host "Recuerda: crea su propio .venv y usa un puerto distinto para el dev server." -ForegroundColor Cyan

    # Abre la consola del usuario en la carpeta nueva (el agente NO hace cd).
    if (-not $NoConsole) { Open-WorktreeConsole -Path $dir }
}

function Get-Worktrees {
    git worktree list
}

function Remove-Worktree {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][int] $Numero,
        [switch] $Force      # descarta cambios sin commitear en el worktree
    )
    $root = Get-RepoRoot
    $repoName = Split-Path $root -Leaf
    $dir = Join-Path (Split-Path $root -Parent) "$repoName-T$Numero"

    if (-not (Test-Path $dir)) { throw "No existe la carpeta: $dir" }

    if ($Force) { git worktree remove --force $dir } else { git worktree remove $dir }
    if ($LASTEXITCODE -ne 0) { throw "git worktree remove fallo (revisa cambios sin commitear o usa -Force)." }

    git worktree prune
    Write-Host "Worktree eliminado: $dir" -ForegroundColor Green
    Write-Host "Si la rama ya esta mergeada, puedes borrarla:  git branch -d ""T#$Numero-<slug>""" -ForegroundColor Cyan
}
