import { usePersonalDetails } from "./layout";
import Link from "next/link";
import styles from "./layout.module.css";

export default function ContactLine() {
  const personalDetails = usePersonalDetails();
  const twitterUrl = `https://twitter.com/${personalDetails.twitter}`;

  return (
    <p>
      I'm on{" "}
      <Link href={twitterUrl}>
        <a className={styles.link}>Twitter</a>
      </Link>{" "}
      and I use email - `{personalDetails.email} at gmail dot com`. I'd love to
      hear from you.
    </p>
  );
}
