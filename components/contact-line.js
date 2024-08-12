import { usePersonalDetails } from "./layout";
import Link from "next/link";
import styles from "./layout.module.css";

export default function ContactLine() {
  const personalDetails = usePersonalDetails();
  const twitterUrl = `https://twitter.com/${personalDetails?.twitter}`;

  return (
    <p>
      I'm on{" "}
      <Link href={twitterUrl}>
        <a className={styles.link}>Twitter</a>
      </Link>{" "}
      and I use email - `{personalDetails.email} at gmail dot com`. I'd love to
      hear from you. <br /> <br /> . <br /> <br /> . <br /> <br /> . <br />{" "}
      <br />
      Like, I <em>actually</em> would. See above about guiltily doing more
      reading than writing. I am the {personalDetails.monarch} of having
      thoughts and questions and being intimidated to put them to an internet
      stranger. You don't have to be. <br /> <br /> . <br /> <br /> . <br />{" "}
      <br /> . <br /> <br />
      But genuinely. Forget about spelling or crafting a topic sentence. Send me
      a knock-knock joke to practice! Drop the activation energy to zero.
    </p>
  );
}
