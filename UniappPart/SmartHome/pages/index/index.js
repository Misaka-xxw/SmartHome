var mqtt = require('../../utils/mqtt.min.js') //根据自己存放的路径修改
const crypto = require('../../utils/hex_hmac_sha1.js'); //根据自己存放的路径修改
var client1
var dvl;
var dvl_2;
Page({
	data: {
		dat1: "",
		dat2: 30,
		dat3: 0,
		touchCount: 0,
	},
	intputone(e) {
		var touchCount = this.data.touchCount + 1;
		this.setData({
			touchCount: touchCount
		});
		console.log(touchCount);
		dvl = e.detail.value;
		console.log(e.touches[0].pageX);
		dvl = e.touches[0].pageX - 55;
		if (dvl > 180) dvl = 180;
		if (dvl < 0) dvl = 0;
		dvl = dvl / 3 + 20;
		this.setData({
			dat2: dvl
		})
		if (touchCount % 10 == 0) {
			client1.publish('/k14ycrf7CgV/J2WYmFiSUIILbhN1v0HS/user/update',
				"\{\"method\":\"thing.service.property.set\",\"id\":\"1590898307\",\"params\":\{\"PowerSwitch_2\":" +
				dvl + "},\"version\":\"1.0.0\"}")
			this.setData({
				touchCount: 0
			});
		}
	},
	intputone2(h) {
		var touchCount = this.data.touchCount + 1;
		this.setData({
			touchCount: touchCount
		});
		console.log(touchCount);
		dvl_2 = h.detail.value;
		console.log(h.touches[0].pageX);
		dvl_2 = h.touches[0].pageX - 55;
		if (dvl_2 > 180) dvl_2 = 180;
		if (dvl_2 < 0) dvl_2 = 0;
		this.setData({
			dat3: dvl_2
		})
		if (touchCount % 10 == 0) {
			client1.publish('/k14ycrf7CgV/J2WYmFiSUIILbhN1v0HS/user/update',
				"\{\"method\":\"thing.service.property.set\",\"id\":\"1590898307\",\"params\":\{\"PowerSwitch\":" +
				dvl_2 + "},\"version\":\"1.0.0\"}")
			this.setData({
				touchCount: 0
			});
		}
	},
	publishshijian(e) {
		client1.publish('/k14ycrf7CgV/J2WYmFiSUIILbhN1v0HS/user/update',
			"\{\"method\":\"thing.service.property.set\",\"id\":\"1590898307\",\"params\":\{\"PowerSwitch\":" +
			dvl + "},\"version\":\"1.0.0\"}")
	},
	publishshijian_2(e) {
		client1.publish('/k14ycrf7CgV/J2WYmFiSUIILbhN1v0HS/user/update',
			"\{\"method\":\"thing.service.property.set\",\"id\":\"1590898307\",\"params\":\{\"PowerSwitch_2\":" +
			dvl_2 + "},\"version\":\"1.0.0\"}")
	},
	onLoad: function() {
		//注意：这里在程序运行后会直接进行连接，如果你要真机调试，记得关掉模拟器或者使用一个按钮来控制连接，以避免模拟器和真机同时进行连接导致两边都频繁断线重连！
		this.doConnect()
	},
	doConnect() {
		const deviceConfig = {
			productKey: "k14ycrf7CgV",
			deviceName: "J2WYmFiSUIILbhN1v0HS",
			deviceSecret: "5a600c30173748483ebb56fe48416cf8",
			regionId: "cn-shanghai" //根据自己的区域替换
		};
		const options = this.initMqttOptions(deviceConfig);
		console.log(options)
		//替换productKey为你自己的产品的（注意这里是wxs，不是wss，否则你可能会碰到ws不是构造函数的错误）
		const client = mqtt.connect('wxs://k14ycrf7CgV.iot-as-mqtt.cn-shanghai.aliyuncs.com', options)
		client1 = client;
		client.on('connect', function() {
			console.log('连接服务器成功')
			//注意：订阅主题，替换productKey和deviceName(这里的主题可能会不一样，具体请查看控制台-产品详情-Topic 类列表下的可订阅主题)，并且确保改主题的权限设置为可订阅
			client.subscribe('/k14ycrf7CgV/J2WYmFiSUIILbhN1v0HS/user/get', function(err) {
				if (!err) {
					console.log('订阅成功！');
				}
			})
			client.publish('/k14ycrf7CgV/J2WYmFiSUIILbhN1v0HS/user/update',
				"\{\"method\":\"thing.service.property.set\",\"id\":\"1590898307\",\"params\":\{\"PowerSwitch\":1},\"version\":\"1.0.0\"}"
				)
		})
		//接收消息监听
		var that = this;

		client.on('message', function(topic, message) {
			// message is Buffer
			let msg = message.toString();
			console.log('收到消息：' + msg);
			//关闭连接 client.end()
			that.setData({
				dat1: msg,
			})
		})
	},
	//IoT平台mqtt连接参数初始化
	initMqttOptions(deviceConfig) {

		const params = {
			productKey: deviceConfig.productKey,
			deviceName: deviceConfig.deviceName,
			timestamp: Date.now(),
			clientId: Math.random().toString(36).substr(2),
		}
		//CONNECT参数
		const options = {
			keepalive: 60, //60s
			clean: true, //cleanSession不保持持久会话
			protocolVersion: 4 //MQTT v3.1.1
		}
		//1.生成clientId，username，password
		options.password = this.signHmacSha1(params, deviceConfig.deviceSecret);
		options.clientId = `${params.clientId}|securemode=2,signmethod=hmacsha1,timestamp=${params.timestamp}|`;
		options.username = `${params.deviceName}&${params.productKey}`;

		return options;
	},

	/*
	  生成基于HmacSha1的password
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
})