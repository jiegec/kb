# 2FA

2FA 指的是 Two factor authentication，核心思想是，基于密码的认证太脆弱，所以要用额外的方法来验证用户。常见的 2FA 方案包括：

1. 短信：国内最熟悉的方案，登录时，除了输入用户名密码，还需要接收短信验证码；实际上，国内很多网站，短信登录已经成为了替代密码的登录方案，不输入用户名密码，直接用手机号和短信验证码登录
2. OTP：通常是 6 位的动态数字密码，或者一串小写英文字母
3. Security Key：以 Yubikey 为代表的硬件密钥

配置 2FA 的时候，通常还会生成一份 Recovery code。目的是如果哪天没办法登录 2FA，例如 Key 不见了，可以用 Recovery code 登录进去。

## OTP

通常是 6 位的动态数字密码，分为 TOTP（Time-based）和 HOTP（HMAC-based）两种，一般会在用 Authenticator App 里面，也有一些硬件的 OTP 设备，例如 [RSA SecurID](https://en.wikipedia.org/wiki/RSA_SecurID)。配置时，通常会输出一个二维码，供 Authenticator App 扫描，读取出里面的 secret，它就可以计算出正确的 OTP 密码。

常见的登录形式是，输入用户名或密码后，提示输入 6 位动态数字密码。一些时候也支持在密码后紧跟 6 位动态密码。

有时 OTP 也不是纯数字，例如 Yubico OTP 就是一串小写字母。此时的操作方法是，输入用户名和密码，不提交，而是长按 Yubikey 的触摸点，那么它就会模拟键盘输入 OTP 并回车。此时密码就会跟着 Yubico OTP 一起发送到服务器，完成认证。

## Security Key

以 Yubikey 为代表的硬件密钥，协议通常是 U2F（早期）或者 CTAP2（比较新），一般是输入用户名密码以后，插入 Security Key 并触摸 Key 上的指定位置，从而完成认证。

U2F 是早期的协议，后来改名为 CTAP 的第一个版本 CTAP1，现在最新版是 CTAP2。除了 CTAP 以外，还有一个用于网站的 API：WebAuthn。开发这些标准的是 FIDO Alliance 组织。

## Passkey/Passwordless

Passkey 或者 Passwordless 其实不能算在 2FA 里面，因为它的目的是，用 Security Key 的技术和 API，去取代密码的存在。它用的其实还是 CTAP 协议和 WebAuthn 的 API，只不过因为替代了密码，所以换了一个好记的名字 `Passkey`。

当然了，它用到了 CTAP2 的新功能：Resident Key/Discoverable Credentials。在 U2F 时代，数据是保存在网站服务端的，用户在网站上登录，网站服务端发送数据给浏览器，浏览器转给 Key，Key 拿到数据以后，根据自己的密钥进行签名，从而实现认证；而有了 Resident Key 以后，Key 也会保存数据，浏览器从 Key 中枚举 Resident Key，根据 metadata，筛选出属于当前访问的网站的数据，再发给 Key，剩下的流程是一样的。这个过程可以阅读 [WebAuthn Resident Key: Discoverable Credentials as Passkeys](https://www.corbado.com/blog/webauthn-resident-key-discoverable-credentials-passkeys)。不过毕竟硬件空间有限，Resident Key 数量也是有限的。

当然了，既然是替代密码（甚至替代用户名），就不能用普通的触摸，而是要用生物认证方法，例如指纹、人脸等等。

此外，原来由物理 Security Key 提供的功能，现在也可以直接在电脑上安全地实现了：利用平台上的一些安全机制，例如 Secure Enclave，TPM 等等，结合 Touch ID/Face ID/Windows Hello 等生物认证系统，提供一个类似 Security Key 的功能。而且在电脑上实现，不太需要考虑 Resident Key 的上限问题。所以某种意义上来说，这是在抢 Yubikey 等 Security Key 的生意。

## 小结

总结下来，其实就是这么一些认证方法：

1. 密码
2. 短信
3. OTP
4. CTAP

视具体情况，可能会要求其中一到多个认证方法。
