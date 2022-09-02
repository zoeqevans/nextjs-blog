import styles from "./betting-charts.module.css";

export default function BettingCharts() {
  const ids_promo_false = [
    "7a3b73f3-b5bf-42e4-af7c-acc7982f24b3",
    "1a698ae3-2dec-457c-be55-75164c1529c9",
    "09bd7951-aab4-4986-95ce-3ce6e1b7e2f4",
  ];
  const ids_promo_true = [
    "73e9de82-54c2-4829-8ea8-55bce709ebf2",
    "1b83c731-97fb-4a64-8a76-89a270bd8061",
    "a8dedc06-ac0e-46f5-8af0-7140295328d7",
  ];

  return (
    <div id="plotly-charts" className={styles.chartsContainer}>
      <div></div>
      <div className={styles.chartsTitle}>
        <p>What Is My Profit When...</p>

        <div className={styles.divider} />
      </div>
      <div></div>
      <div className={styles.colTitle}>
        Risk Aversion = 1 <br />
        (Losses And Gains Treated Equally)
      </div>
      <div className={styles.colTitle}>
        Risk Aversion = 2 <br />
        (Normal)
      </div>
      <div className={styles.colTitle}>
        Risk Aversion = 100 <br />
        (Any Loss is Unacceptable)
      </div>
      <div className={styles.rowLabel}>
        The Bet Token <strong>does not</strong> return its stake upon winning
      </div>
      {ids_promo_false.map((id) => (
        <div id={id} key={id} className="plotly-chart-div" />
      ))}
      <div className={styles.rowLabel}>
        The Bet Token <strong>does</strong> return its stake upon winning
      </div>
      {ids_promo_true.map((id) => (
        <div id={id} key={id} className="plotly-chart-div" />
      ))}
    </div>
  );
}
