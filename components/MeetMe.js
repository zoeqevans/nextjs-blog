import Image from "next/image";
import styles from "../styles/Home.module.css";
import { firstName } from "./layout";

const MeetMe = () => {
  return (
    <div>
      <Image
        src="/images/profile.jpg"
        alt={`${firstName} Evans avatar`}
        width={150}
        height={150}
        className={styles.img}
      />
      <p className={styles.p}>
        Hey, I am <strong>John Doe</strong>. I love coding. Lorem ipsum dolor
        sit, amet consectetur adipisicing elit. Reiciendis commodi numquam
        incidunt blanditiis quibusdam atque natus inventore sunt autem iusto.
      </p>
    </div>
  );
};

export default MeetMe;
