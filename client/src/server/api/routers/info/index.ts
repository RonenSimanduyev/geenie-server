import { z } from "zod";
import { publicProcedure, createTRPCRouter } from "../../trpc";
import { getReviews } from "./reviews";
import { GoogleAuth } from "google-auth-library";
import { google } from "googleapis";
import { gptClient } from "./gpt";
import path from "path";

export default createTRPCRouter({
  fetch: publicProcedure.input(z.string()).mutation(async ({ input, ctx }) => {
    const prevResponse = await ctx.prisma.chatResponse.findUnique({
      where: {
        asin: input,
      },
      select: {
        response: true,
      },
    });
    if (prevResponse) {
      return prevResponse.response;
    }
    const jsonDir = path.join(process.cwd(), "json");
    const credentials = path.join(jsonDir, "credentials.json");
    const authClient = new GoogleAuth({
      keyFile: credentials,
      scopes: ["https://www.googleapis.com/auth/drive"],
    });
    const drive = google.drive({ version: "v3", auth: authClient });
    const file = await drive.files.list({
      q: `name = '${input}.json' and '13OFCt9ijeowKRwHcRv8yWWvKbTJwm2KE' in parents`,
    });
    let prevFileId: string | undefined;
    if (file?.data?.files?.length) {
      prevFileId = file?.data?.files?.[0]?.id ?? undefined;
    }
    if (!prevFileId) {
      const reviews = await getReviews(input);
      const res = await drive.files.create({
        requestBody: {
          name: `${input}.json`,
          mimeType: "application/json",
          parents: ["13OFCt9ijeowKRwHcRv8yWWvKbTJwm2KE"],
        },
        media: {
          mimeType: "application/json",
          body: JSON.stringify(reviews),
        },
      });
      if (!res.data.id) throw new Error("No ID returned from Google Drive");
      prevFileId = res.data.id;
    }
    const url = `https://drive.google.com/file/d/${prevFileId}/view?usp=sharing`;
    const res = await gptClient.sendMessage(
      `summarize the complaints from the reviews below this link: ${url}\n\n\n\n\nPlease write in academic writing style, English language.`
    );
    await ctx.prisma.chatResponse.create({
      data: {
        response: res.text,
        asin: input,
        reviewsUrl: url,
      },
    });
    return res.text;
  }),
});
