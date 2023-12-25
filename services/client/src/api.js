// Websocket API

const getWebSocket = () => {
  if (import.meta.env.DEV){
      return "ws://localhost:13345";
  }
  // TODO: use env variables
  return "wss://racm-monitor.cires-ac.net/wsocket/";
    // Below config works locally
  // return "wss://localhost/wsocket/";
}

export const WebsocketUri = getWebSocket();

// Auth API
export const baseUrl = "/api/v1";
// Auth endpoints
export const changePasswordUrl = baseUrl + "/change_password/";
export const confirmUrl = baseUrl + "/confirm/"
export const stationsUrl = baseUrl + "/stations/";
export const tokensUrl = baseUrl + "/tokens/";
export const registerUrl = baseUrl + "/new_user/";
export const reconfirmUrl = baseUrl + "/confirm";
export const resetUrl = baseUrl + "/reset";
export const resetPasswordUrl = baseUrl + "/reset/"
