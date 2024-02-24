export const WebsocketUri = import.meta.env.VITE_WEBSOCKET_DOMAIN;

// Auth API
export const baseUrl = import.meta.env.VITE_API_DOMAIN + "/api/v1";
// Auth endpoints
export const changePasswordUrl = baseUrl + "/change_password/";
export const confirmUrl = baseUrl + "/confirm/"
export const tokensUrl = baseUrl + "/tokens/";
export const registerUrl = baseUrl + "/new_user/";
export const reconfirmUrl = baseUrl + "/confirm";
export const resetUrl = baseUrl + "/reset";
export const resetPasswordUrl = baseUrl + "/reset/"
