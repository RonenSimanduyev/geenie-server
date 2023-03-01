import { type NextPage } from "next";
import Head from "next/head";
import { useState } from "react";
import { Elipse, Spinner } from "~/components";

import { api } from "~/utils/api";

const Home: NextPage = () => {
  const [URL, setURL] = useState("");
  const [GPTRespone, setGPTRespone] = useState("")
  const getInfo = api.info.fetch.useMutation();

  const sendLink = async () => {
    const response = await fetch('http://127.0.0.1:8000/fullScript', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain' },
      body: JSON.stringify({ URL })
    });

    const data = await response.json();
    setGPTRespone(data)

  };

  return (
    <>
      <Head>
        <title>GeenieAI - Reviews</title>
        <meta name="description" content="Reviews Testing For Geenie AI" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="flex w-full flex-col items-center gap-2">
        <div className="lin relative flex h-[500px] w-full flex-col items-center gap-4 p-3">
          <div className="absolute top-12 -left-4 z-[-1]">
            <Elipse />
          </div>
          <div className="absolute top-3 -right-5 z-[-1]">
            <Elipse />
          </div>
          <h1 className="mt-8 text-center font-Montserrat text-3xl font-bold text-blackish">
            Unlock the Power of Amazon Product Reviews
          </h1>
          <p className="mt-4 max-w-[40rem] text-center font-Montserrat text-xl font-bold text-blackish">
            Make AI work for you with one click access to thousands of reviews,
            understand consumer sentiment and compare your product to
            competitors.
          </p>
          <div className="shadowStuff mt-6 flex w-[813px] items-center gap-2 rounded-md bg-white p-2.5">
            <input
              className="w- w-[80%] rounded-xl border border-grayish p-2.5 font-Montserrat text-blackish placeholder:text-grayish focus:outline-none"
              placeholder="Paste your Amazon URL or URL here"
              value={URL}
              onChange={(e) => setURL(e.currentTarget.value)}
            />
            <button
              onClick={() => {
                getInfo.mutate(URL), sendLink();
              }}
              className={`shadowStuff flex h-[40px] w-[130px] items-center justify-center gap-2 rounded-lg bg-blue ${getInfo.isLoading ? "text-sm" : "text-lg"
                } font-bold text-white`}
            >
              Run Report {getInfo.isLoading ? <Spinner sm /> : null}
            </button>
          </div>
          {GPTRespone}
        </div>
        <div className="flex flex-wrap items-center justify-center gap-2">
          {getInfo.data ? (
            <code className="font-Montserrat text-sm text-blackish">
              {getInfo.data}
            </code>
          ) : null}

        </div>

      </main>
    </>
  );
};

export default Home;
