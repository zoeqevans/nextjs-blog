import Head from "next/head";
import Script from "next/script";
import Link from "next/link";
import Date from "../components/date";
import Layout, { usePersonalDetails } from "../components/layout";
import utilStyles from "../styles/utils.module.css";
import { getSortedPostsData } from "../lib/posts";

export default function Home({ allPostsData }) {
  const personalDetails = usePersonalDetails();
  const siteTitle = personalDetails?.fullName;

  return (
    <Layout home>
      <Head>
        <title>{siteTitle}</title>
      </Head>
      <section className={utilStyles.postPreview}>
        <div className={utilStyles.smallTitle}>
          <Link href="/sports-betting">
            <a>
              How I Paid My Rent Betting on Basketball... Without Knowing the
              Rules
            </a>
          </Link>
        </div>
        <div className={utilStyles.smallTitleDate}>September 2nd, 2022</div>
      </section>
    </Layout>
  );
}

// export async function getStaticProps() {
//   const allPostsData = getSortedPostsData();
//   return {
//     props: {
//       allPostsData,
//     },
//   };
// }
