Chatbot-facebook-demo (in development)
===
> **Note**
> **Đọc thêm tài liệu về aiohtpp?** https://docs.aiohttp.org/en/stable/

## :computer: Đăng ký Meta for Developers Programs

Truy cập https://developers.facebook.com và tiến hành đăng ký phát triển, tạo ứng dụng trên Meta. Lúc này sau khi truy cập vào Graph Explorer, Meta sẽ cung cấp cho bạn Facebook Fanpage API cũng như User API để tiến hành phát triển các app của riêng mình.

## :arrow_up_small: Chọn cho mình một nền tảng để host (và deploy)
> Nếu bạn dùng một nền tảng khác (như Netlify) thì thao tác cũng sẽ tương tự ở các bước git push lên, chắc sẽ có khác biệt ở bước tạo tài khoản thôi.
> 
Ở đây thật ra có nhiều option nhưng do chưa tìm hiểu kỹ (hoặc do mình không có tiền vì có khá nhiều nền tảng yêu cầu Pricing vài trăm $/năm chỉ để host :cry: ), mình quyết định chọn Heroku vì thao tác khá dễ và các lệnh trong Terminal để thao tác với nó khá giống với Github nên theo mình thì nó khá dễ dùng. :face_with_hand_over_mouth: 


---

**:bulb: Setup Heroku (hoặc Netlify - recommend nên thử)**
Cài đặt package **heroku-cli** nếu bạn chưa cài đặt:
```console=
curl "https://cli-assets.heroku.com/install.sh" | sh
```
Arch-based:
```console=
yay -S heroku-cli
```
Mở cửa sổ trình duyệt và đăng ký Heroku free:
```console=
heroku login 
echo "Nhấn phím bất kỳ để mở cửa sổ web"
````
> Đăng ký xong xác thực và đăng nhập vào rồi đóng trình duyệt đi. Chỉ sau khi đăng nhập ta mới git push lên branch của app trên heroku được.

Tạo một app bằng giao diện web của Heroku hoặc bằng lệnh:
```console= 
heroku apps:create <APPNAME>
```
Dùng git để push lên branch master của app vừa tạo.
```console=
git init
```
```console=
git add .
```
```console=
git push heroku master
```
Đợi Heroku deploy app của bạn lên hệ thống. Nếu gặp lỗi thì ta nên đổi phiên bản của Python trong file `runtime.txt` từ `3.10.x` sang `3.9.3` vì đây là phiên bản ổn định của Python, các app vẫn chưa support ổn định trên `3.10.x`.
> Lưu ý rằng khi đổi như thế thì cũng cần phải đổi Stack Heroku. Stack mới nhất của Heroku không support Python `3.9.3`. Mình đang dùng `heroku-stack-20`.

## :rocket: Tiến hành Setup bot cho Fanpage của bạn

Truy cập Meta for Developers và tạo một app, có thể để tên giống app của Heroku (hoặc app của nền tảng mà bạn đã chọn để host), quăng địa chỉ URL của app mà bạn đã host vào mục Callback URL của Webhook có tên `messages` ngay tại Fanpage mà bạn muốn cài đặt chatbot.
###### tags: `Heroku` `Documentation` `Facebook` `Meta` `Chatbot`