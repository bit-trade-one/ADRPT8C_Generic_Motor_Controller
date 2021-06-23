# ADRPTB8C　ラズベリー・パイ専用汎用モータ制御基板“汎用電動機制御基板”

ソフトウェアエンジニアにこそ使っていただきたい！  
はんだ付け不要、安心・安全の汎用モータ制御基板  

![](http://btoshop.jp/wp-content/uploads/sites/3/2017/08/WP-%E8%A3%BD%E5%93%81%E7%B4%B9%E4%BB%8BM29-ADRPTB8C.png)  

## 製品詳細は[こちら](https://bit-trade-one.co.jp/product/module/adrptb8c/)!

## 実験ページ（ソフトウェア等もこちらで公開中）
[[ハードウェア編]](https://bit-trade-one.co.jp/blog/20170913/)!
[[ソフトウェア編]](https://bit-trade-one.co.jp/blog/2017091301/)!
[[NodeRed編]](https://bit-trade-one.co.jp/blog/2017091903/)!

## [回路図](https://github.com/bit-trade-one/ADRPT8C_Generic_Motor_Controller/blob/master/Schematics/raspi-bench_v11p_schematics.pdf)

## 製品仕様
【汎用入出力】デジタル入出力6ch ラズベリーパイのGPIO 入出力範囲：0～3.3V  
・アナログ入力　6ch、12bit 入力範囲：0～3.3V  ・アナログ入力　2ch、12bit 入力範囲：0～6.6V  
　※デジタル入出力（GPIO）6chとアナログ入力6chは同時使用出来ません。  

・アナログ入力6ch：MCP3208　12bit　8ch　A/Dコンバータ　SPI  
　　　　　　　　　　　サンプリング速度：50ｋsps　入力範囲：0～3.3V  

・アナログ入力2チャネル  
　　　　　　　　　　・MCP3208　12bit　8ch　A/Dコンバータ　SPI  
　　　　　　　　　　　サンプリング速度：50ｋsps　入力範囲：0～6.6V  

【PWM出力】8ch：PCA9685　12bitPWM、16ch（内6chをTB6612に使用）I2C  
＊PWM出力でサーボモータを制御する場合、DCモータとの同時使用は、ソフト的に難易度が高くなります。  
サーボモータと、DCモータを同時使用の場合、スタックでの使用を推奨します。  

【モータ出力】2ch：出力電流　1.2A　TB6612　Dual　DCモータ・ドライバ  
　　　　　　　　　　正転/逆転/ショートブレーキ/ストップ制御機能付き  
　　　　　　　　　　ＰＷＭ出力：PCA9685により制御  
3.3V、5Vの両電圧系に対応  
　　　・3.3V  I2C：ラズパイからの直接信号（2.7ｋΩプルアップ済み）  
　　　・5V  I2C：PCA9517　レベル変換　I2C　Repeater  

PWM用電源、モータ用電源を外部から供給可能  
　・PWM用電源：5V  
　・モータ用電源：5～12V  
　・内部電源との選択は、ボード上のピンヘッダで行う  

【コネクタ部】  
【汎用入出力】　6ch　3ピン（SIG+3.3V+GND）/ch（24極スクリューレス端子台を使用）  
【アナログ入力】　2ch　3ピン（SIG/+5V/GND）/ch（24極スクリューレス端子台を使用）  
【ＰＷＭ出力】　8ch　3ピン（SIG+5V+GND）/ch 　2.54pitch、ピンヘッダ  
【モータ出力】　2ch　2ピン（SIG+、SIG-）/ch　(2極スクリューレス端子台を2個使用)  
3.3V、5V両対応：I2C  
　　　3.3V用I2C　4ピン（3.3V、SCL、SDA、GND）/ch　2.54pitch、ピンヘッダ  
　　　5V用I2C　4ピン（5V、SCL、SDA、GND）/ch　2.54pitch、ピンヘッダ  

【外部電源入力】  
　・PWM用電源：2極スクリューレス端子台  
　・モータ用電源：2極スクリューレス端子台  

【本体重量】　約39g  
【サイズ】W64×D71×H22mm(突起物除く)  
【付属品】　　スペーサM2.6ｘ13mm 4本　ネジM2.6ｘ6mm 8本    保証書1部（Raspberry Pi本体は付属しません）  
【保証期間】お買い上げから1年間  
【使用温度】0 ～ 40℃（結露なきこと）  
【生産国】Made in Japan  
