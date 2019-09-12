<#
.SYNOPSIS
    Retrieve data for one or more Phish shows

.DESCRIPTION
    This function will query the phish.net api for show data based on input parameters. 
    A phish.net account and API key are required to access this data. 
    Account registration can be submitted here: http://phish.net/register
    API registration can be submitted here: http://api.phish.net/

.PARAMETER APIKey
    Your Private API Key

.PARAMETER Year
    Year to query (1983-present)

.EXAMPLE
    PS C:\> Get-PhishShow -APIKey '1234567890' -Year 1983

    showid       : 1251253531
    showdate     : 1983-12-03
    billed_as    : Phish
    link         : http://phish.net/setlists/phish-december-03-1983-marsh-austin-tupper-dormitory-university-of-vermont-burlington-vt-usa.html
    location     : Burlington, VT, USA
    venue        : Marsh / Austin / Tupper Dormitory, University of Vermont
    setlistnotes : This show, played by Trey, Mike, Fish, and Jeff, may have been billed as &ldquo;Blackwood Convention.&rdquo; This date is believed to be correct 
    but, due to a lack of records, the exact date cannot be ascertained. &nbsp; &nbsp;
    venueid      : 272
    tourid       : 1
    tourname     : 1983 Tour
    tour_when    : 1983
    artistlink   : http://phish.net/setlists/phish
    artistid     : 1
#>

Function Get-PhishShow {
    Param(
        [Parameter(Mandatory = $true)]
        [string]$APIKey,
        [string]$Year = '1983'
    )
    $BaseURI = 'https://api.phish.net/v3/shows/query?apikey='
    $QueryURI = $BaseURI + $APIKey + '&year=' + $year
    $QueryResults = Invoke-RestMethod -Method Post -Uri $QueryURI -ContentType 'application/json'
    $Data = $QueryResults.response.data
    Return $Data
}
