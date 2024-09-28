<template>
	<view class="container">
		<view class="header">
			<text>🐾智能家居~下拉刷新~🐾</text>
		</view>
		<uni-card title="💡灯控制">
			<view style="display: flex; flex-direction: row; padding-right:20rpx ;">
				<text>开关\t</text>
				<zero-switch class='inline_item' v-model="lightSwitch" @change="pushLightSwitch()" :moon="true"
					backgroundColorOff='#0055ff' backgroundColorOn="#aaffff"></zero-switch>
			</view style="display: flex; flex-direction: row;">
			<view>
				<text>亮度调节\t</text>
				<slider v-model="lightBrightness" @change="handleLightBrightnessChange" min="0" max="10"
					active-color="#0055ff" /> <!-- activeColor 绑定滑动条颜色 -->
			</view>
			<button @click="" style="flex: 1;">➕添加定时开关</button>
		</uni-card>
		<uni-card title="🌡温湿度信息">
			<view>
				<text style="color: red;">{{ temperature }}°C</text>
				<text>\t/\t</text>
				<text style="color: blue;">{{ humidity }}%</text>
			</view>
		</uni-card>
		<uni-card title="🚨红外检测">
			<text>{{ infraredStatus }}</text>
		</uni-card>
		<uni-card title="💙蓝牙连接与网络设置">
			<uni-easyinput v-model="wifi_id" focus placeholder="请输入wifi账号" style="box-shadow: 1px 1px 3px grey;margin: 10px;"></uni-easyinput>
			<uni-easyinput type="password" v-model="wifi_pwd" placeholder="请输入密码" style="box-shadow: 1px 1px 3px grey;margin: 10px;"></uni-easyinput>
			<!-- <input type="text" style="box-shadow: 1px 1px 3px grey;margin: 10px;"> -->
			<button @click="handleBluetoothConnection" style="flex: 1;">连接蓝牙</button>
		</uni-card>
		<uni-card title="⚙模块管理">
			<view style="display: flex; flex-direction: row;">
				<button @click="handleNewExtensionModule" style="flex: 1;">➕︎新建</button>
				<button @click="handleNewExtensionModule" style="flex: 1;">🖊编辑</button>
			</view>
		</uni-card>
	</view>
</template>

<script>
	import mqtt from '../../utils/mqtt.min.js';
	import crypto from '../../utils/hex_hmac_sha1.js';
	export default {
		data() {
			return {
				refreshing: false,
				lightSwitch: false,
				lightBrightness: 0,
				activeColor: '',
				temperature: 0,
				humidity: 0,
				infraredStatus: '未检测',
				deviceConfig: {
					productKey: "",
					deviceName: "wx-uni-app",
					deviceSecret: "",
					regionId: "cn-shanghai"
				},
				// device: null,
				client1: null,
				iot: null,
				use_sdk: false,
				wifi_id: "",
				wifi_pwd: ""
			};
		},
		methods: {
			// 处理下拉刷新
			onRefresh() {
				// 在此处编写下拉刷新的逻辑
				this.refreshing = true;
				// 模拟刷新操作
				//延时2秒
				setTimeout(() => {
					this.refreshing = false;
				}, 2000);
			},
			myPost(paramName, value) {
				if (typeof value == "string")
					value = '"' + value + '"';
				else if (typeof value == "boolean")
					value = Number(value);
				var topic1 = `/${this.deviceConfig.productKey}/${this.deviceConfig.deviceName}/user/update`
				var topic =
					`/sys/${this.deviceConfig.productKey}/${this.deviceConfig.deviceName}/thing/event/property/post`;
				var info =
					`{"id": "123","version":"1.0.0","sys":{"ack":0},"params":{"${paramName}":${value}},"method": "thing.event.property.post"}`;
				this.client1.publish(topic, info);
			},
			// 处理灯开关状态变化
			pushLightSwitch() {
				this.myPost("LightSwitch", this.lightSwitch);
				// this.client1.publish(
				// 	`/${this.deviceConfig.productKey}/${this.deviceConfig.deviceName}/user/update`,
				// 	`{"method":"thing.service.property.set","id":"787926721","params":{"LightBrightness":1},"version":"1.0.0"}`
				// );
			},
			// 处理灯亮度滑块变化
			handleLightBrightnessChange(value) {
				// console.log(this.lightBrightness)
				// let red = Math.floor(this.lightBrightness * 25.5);
				// let green = 255 - Math.floor(this.lightBrightness * 2.55);
				// let blue = 0;
				// // 生成颜色值（格式为 #RRGGBB）
				// this.activeColor =
				// 	`#${red.toString(16).padStart(2, '0')}${green.toString(16).padStart(2, '0')}${blue.toString(16).padStart(2, '0')}`;
				// console.log(this.activeColor)
				this.myPost("LightBrightness", this.lightBrightness);
			},
			// 处理蓝牙连接按钮点击
			handleBluetoothConnection() {

			},
			// 处理新建扩展模块按钮点击
			handleNewExtensionModule() {

			},
			doConnect() {
				const options = this.initMqttOptions(this.deviceConfig);
				console.log(options)

				const client = mqtt.connect(`wxs://${this.deviceConfig.productKey}.iot-as-mqtt.cn-shanghai.aliyuncs.com`,
					options);
				this.client1 = client;
				client.on('connect', () => {
					console.log('连接服务器成功');
					// 订阅主题
					client.subscribe(`/${this.deviceConfig.productKey}/${this.deviceConfig.deviceName}/user/get`, (
						err) => {
						if (!err) {
							console.log('订阅成功！');
						}
					});
					client.subscribe(
						`/${this.deviceConfig.productKey}/${this.deviceConfig.deviceName}/user/update`, (
							err) => {
							if (!err) {
								console.log('订阅成功！');
							}
						});
					client.subscribe(
						`/sys/${this.deviceConfig.productKey}/${this.deviceConfig.deviceName}/thing/event/property/post`,
						(err) => {
							if (!err) {
								console.log('订阅成功！');
							}
						});
				});
				// 接收消息监听
				client.on('message', (topic, message) => {
					// message is Buffer
					let msg = message.toString();
					console.log('收到topic：' + topic.toString())
					console.log('收到消息：' + msg);
				});
			},
			// IoT 平台 mqtt 连接参数初始化
			initMqttOptions(deviceConfig) {
				const params = {
					productKey: deviceConfig.productKey,
					deviceName: deviceConfig.deviceName,
					timestamp: Date.now(),
					clientId: Math.random().toString(36).substr(2),
				};
				// CONNECT 参数
				const options = {
					keepalive: 60, // 60s
					clean: true, // cleanSession 不保持持久会话
					protocolVersion: 4 // MQTT v3.1.1
				};
				options.password = this.signHmacSha1(params, deviceConfig.deviceSecret);
				options.clientId = `${params.clientId}|securemode=2,signmethod=hmacsha1,timestamp=${params.timestamp}|`;
				options.username = `${params.deviceName}&${params.productKey}`;
				return options;
			},
			/*
			  生成基于 HmacSha1 的 password
			  参考文档：https://help.aliyun.com/document_detail/73742.html?#h2-url-1
			*/
			signHmacSha1(params, deviceSecret) {
				let keys = Object.keys(params).sort();
				// 按字典序排序
				keys = keys.sort();
				const list = [];
				keys.map((key) => {					
					list.push(`${key}${params[key]}`);
				});
				const contentStr = list.join('');
				return crypto.hex_hmac_sha1(deviceSecret, contentStr);
			}
		},
		parseData(data) {
			const dataObject = JSON.parse(data);
			const items = dataObject.items;
			return items;
		},
		whichInMessage(data) {
			const items = parseData(data);
			if (items.hasOwnProperty("LightBrightness")) {
				this.LightBrightness = items.LightBrightness;
			}
			
			
			
			
			for (const key in items) {
				if (items.hasOwnProperty(key)) {
					console.log(`key:${key}, value:${items[key].value}`);
					//this.myPost(key,items[key])
				}
			}
			if (items.hasOwnProperty(key)){}
			
		},
		onLoad() {
			this.doConnect();
			uni.openBluetoothAdapter({
				success: function(res) {
					console.log('是否开启蓝牙', res)
				},
				fail: function(msg) {
					console.log(msg)
				}
			})

		}
	};
</script>

<style>
	.container {
		padding: 20px;
		background-color: #f5f5f5;
	}

	.header {
		padding: 10px;
		background-color: #e0e0e0;
	}

	.uni-card {
		margin-bottom: 20px;
		padding: 15px;
		/* background-color: #fff; */
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.uni-card.title {
		font-size: 18px;
		font-weight: bold;
		margin-bottom: 10px;
	}
</style>