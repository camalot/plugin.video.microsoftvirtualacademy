if ( $env:APPVEYOR_REPO_BRANCH -eq "master" -and $env:APPVEYOR_PULL_REQUEST_NUMBER -eq $null ) {
  $env:CI_DEPLOY_GITHUB = $true;
} elseif ( $env:APPVEYOR_REPO_BRANCH -eq "develop" -and $env:APPVEYOR_PULL_REQUEST_NUMBER -eq $null ) {
  $env:CI_DEPLOY_GITHUB_PRE = $true;
  $env:CI_DEPLOY_GITHUB = $false;
} else {
  $env:CI_DEPLOY_GITHUB = $false;
}
