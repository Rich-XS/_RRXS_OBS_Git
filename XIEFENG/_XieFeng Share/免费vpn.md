
free [[VPN]]

Warp + 下载和开通：
https://bittly.cc/BDX8D
https://www.youtube.com/watch?v=mkv6MRzvjPE
1.1.1.1
linux
curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflare-client.list

sudo apt-get update 
sudo apt-get install cloudflare-warp

# Install
sudo apt-get update && sudo apt-get install cloudflare-warp

![[Pasted image 20250705093457.png]]



[nthLink](https://www.downloadnth.com/download.html)
![[nthlink-win64-current.exe]]