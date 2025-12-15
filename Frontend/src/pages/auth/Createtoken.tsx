import FingerprintJS from '@fingerprintjs/fingerprintjs';


const create_token = async () => {
    const tk = await FingerprintJS.load();
    const result = await tk.get()
    sessionStorage.setItem("user_token", result.visitorId);
    return result.visitorId;
}
export default create_token;