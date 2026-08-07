[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$InputDocx,
    [Parameter(Mandatory)][string]$OutputPdf
)

$inputPath = (Resolve-Path -LiteralPath $InputDocx).Path
$outputPath = [System.IO.Path]::GetFullPath($OutputPdf)
$word = $null
$document = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $document = $word.Documents.Open($inputPath, $false, $true)
    $document.ExportAsFixedFormat($outputPath, 17)
} finally {
    if ($null -ne $document) { $document.Close($false) }
    if ($null -ne $word) { $word.Quit() }
    if ($null -ne $document) {
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($document)
    }
    if ($null -ne $word) {
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)
    }
    $document = $null
    $word = $null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
Write-Output "Exported PDF successfully."
