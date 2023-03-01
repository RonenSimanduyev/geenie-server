import parse from "node-html-parser";
import { COOKIE, MIN_REVIEWS } from "./constants";

export type IReview = {
  rating: string | undefined;
  title: string | undefined;
  date: string | undefined;
  body: string | undefined;
  verified: boolean;
  name: string | undefined;
};

export async function getReviews(
  asin: string,
  page = 1,
  prev: IReview[] = []
): Promise<IReview[]> {
  try {
    const results = await fetch(
      `https://www.amazon.com/product-reviews/${asin}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=${page}`,
      {
        headers: {
          cookie: COOKIE,
          "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        },
      }
    );
    const $ = parse(await results.text());
    const reviews = $.querySelectorAll(".a-section.review.aok-relative");
    const reviewData = reviews.map((review) => {
      const rating = review.querySelector(".a-icon-alt")?.text;
      const title = review.querySelector(".review-title")?.text;
      const date = review.querySelector(".review-date")?.text;
      const body = review.querySelector(".review-text")?.text;
      const verified = review.querySelector(".a-declarative") ? true : false;
      const name = review.querySelector(".a-profile-name")?.text;
      return {
        rating: rating?.trim(),
        title: title?.trim(),
        date: date?.trim(),
        body: body?.trim().startsWith("The media could not be loaded.")
          ? "No Media"
          : body?.trim(),
        verified: verified,
        name: name?.trim(),
      };
    });
    const allReviews = [...prev, ...reviewData];
    if (allReviews.length < MIN_REVIEWS && reviewData.length > 0) {
      return await getReviews(asin, page + 1, allReviews);
    }
    return allReviews;
  } catch {
    return prev;
  }
}
