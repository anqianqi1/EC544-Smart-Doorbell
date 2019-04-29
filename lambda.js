var AWS = require('aws-sdk');
var iotdata = new AWS.IotData({endpoint: 'a2ccd2xwv31ide-ats.iot.us-east-1.amazonaws.com'});
exports.handler = function(event, context) {
 
    var params = {
        topic: 'freertos/demos/echo',
        payload:  `${"RUN"}`,
        qos: 0
        };
        
 
    iotdata.publish(params, function(err, data){
        if(err){
            console.log(err);
        }
        else{
            console.log("success?");
            //context.succeed(event);
        }
    });
    
};
