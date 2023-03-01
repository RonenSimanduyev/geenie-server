import { ChatGPTUnofficialProxyAPI } from "chatgpt";
import { env } from "~/env.mjs";

export const gptClient = new ChatGPTUnofficialProxyAPI({
  accessToken: env.OPENAI_ACCESS_TOKEN,
  apiReverseProxyUrl: "https://chat.duti.tech/api/conversation",
});
