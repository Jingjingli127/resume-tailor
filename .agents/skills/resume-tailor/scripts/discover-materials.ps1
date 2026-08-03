[CmdletBinding()]
param(
    [Parameter()][string]$WorkspaceRoot = (Get-Location).Path,
    [Parameter()][switch]$AsJson
)

$root = (Resolve-Path -LiteralPath $WorkspaceRoot).Path
$skillPath = Join-Path $root '.agents\skills\resume-tailor'

$files = Get-ChildItem -LiteralPath $root -Recurse -File -ErrorAction Stop |
    Where-Object {
        $_.FullName -notlike "$skillPath*" -and
        $_.FullName -notmatch '[\\/]__MACOSX[\\/]' -and
        $_.Name -notlike '~$*'
    }

$storyDocs = @($files | Where-Object {
    $_.Extension -ieq '.docx' -and
    ($_.BaseName -match '(?i)complete[ _-]*story|project[ _-]*complete')
} | Select-Object -ExpandProperty FullName)

$resumeDocs = @($files | Where-Object {
    $_.Extension -ieq '.docx' -and $_.BaseName -match '(?i)resume'
} | Select-Object -ExpandProperty FullName)

$imageExtensions = @('.png', '.jpg', '.jpeg', '.heic', '.webp', '.gif', '.tif', '.tiff')
$imageFiles = @($files | Where-Object {
    $imageExtensions -contains $_.Extension.ToLowerInvariant()
} | Select-Object -ExpandProperty FullName)

$jdFolders = @(Get-ChildItem -LiteralPath $root -Recurse -Directory -ErrorAction Stop |
    Where-Object { $_.Name -match '(?i)^job[ _-]*descriptions?$|^jds?$' } |
    Select-Object -ExpandProperty FullName)

$result = [ordered]@{
    workspace_root = $root
    project_story_documents = $storyDocs
    resume_documents = $resumeDocs
    supporting_images = $imageFiles
    job_description_folders = $jdFolders
}

if ($AsJson) {
    $result | ConvertTo-Json -Depth 4
} else {
    [pscustomobject]@{
        WorkspaceRoot = $root
        ProjectStories = $storyDocs.Count
        Resumes = $resumeDocs.Count
        SupportingImages = $imageFiles.Count
        JobDescriptionFolders = $jdFolders.Count
    }
}
