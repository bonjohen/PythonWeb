# PowerShell script to generate self-signed SSL certificates for development

# Create directory for certificates
New-Item -Path "nginx/ssl" -ItemType Directory -Force | Out-Null

# Generate a self-signed certificate
$cert = New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "cert:\LocalMachine\My"

# Export the certificate
$certPassword = ConvertTo-SecureString -String "password" -Force -AsPlainText
$certPath = "nginx/ssl/cert.pfx"
Export-PfxCertificate -Cert $cert -FilePath $certPath -Password $certPassword | Out-Null

# Convert PFX to PEM format for the certificate
$pemCertPath = "nginx/ssl/cert.pem"
$pemKeyPath = "nginx/ssl/key.pem"

# Use OpenSSL to convert the certificate (requires OpenSSL to be installed)
# If OpenSSL is not installed, you'll need to install it or use a different method
try {
    # Extract the certificate
    openssl pkcs12 -in $certPath -clcerts -nokeys -out $pemCertPath -password pass:password
    
    # Extract the private key
    openssl pkcs12 -in $certPath -nocerts -out $pemKeyPath -password pass:password -passout pass:password
    
    # Remove the passphrase from the private key
    $tempKeyPath = "nginx/ssl/temp_key.pem"
    openssl rsa -in $pemKeyPath -out $tempKeyPath -passin pass:password
    Move-Item -Path $tempKeyPath -Destination $pemKeyPath -Force
    
    Write-Host "Self-signed SSL certificates generated successfully!"
    Write-Host "Certificate: $pemCertPath"
    Write-Host "Private key: $pemKeyPath"
}
catch {
    Write-Host "Error: OpenSSL is required to convert the certificate to PEM format."
    Write-Host "Please install OpenSSL and make sure it's in your PATH, or convert the certificate manually."
    Write-Host "Certificate (PFX format): $certPath"
}
