<script>
import Summary from "/summary/card.json"

export default {
  methods: {
    input_code() {
      const link_address = window.prompt("Paste the link address of `Select this account`")
      const session_token_code = RegExp("de=(.*)&").exec(link_address)[1]
      this.get_session_token(session_token_code)
    },
    authorize(){
      window.open(this.authorize_url, "_blank")
    },
    get_session_token(session_token_code) {
      const url = "https://a9o2idgf8d.execute-api.ap-northeast-1.amazonaws.com/dev/session_token"
      const header = {
        "Content-Type": "application/json",
      }
      const body = {
        session_token_code: session_token_code
      }
      const response = fetch(url, {
        method: "POST",
        headers: header,
        body: JSON.stringify(body)
      })
      .then(r => r.json())
      .then(payload => {
        this.get_access_token(payload)
      })
    },
    get_access_token(payload) {
      const url = "https://a9o2idgf8d.execute-api.ap-northeast-1.amazonaws.com/dev/access_token"
      const header = {
        "Content-Type": "application/json",
      }
      const response = fetch(url, {
        method: "POST",
        headers: header,
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(payload => {
        console.log(payload)
        this.get_splatoon_token(payload)
      })
    },
    get_splatoon_token(payload) {
      const url = "https://a9o2idgf8d.execute-api.ap-northeast-1.amazonaws.com/dev/splatoon_token"
      const header = {
        "Content-Type": "application/json",
      }
      const response = fetch(url, {
        method: "POST",
        headers: header,
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(payload => {
        console.log(payload)
        this.get_splatoon_access_token(payload)
      })
    },
    get_splatoon_access_token(payload) {
      const url = "https://a9o2idgf8d.execute-api.ap-northeast-1.amazonaws.com/dev/splatoon_access_token"
      const header = {
        "Content-Type": "application/json",
      }
      const response = fetch(url, {
        method: "POST",
        headers: header,
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(payload => {
        console.log(payload)
        this.get_iksm_session(payload)
      })
    },
    get_iksm_session(payload) {
      const url = "https://a9o2idgf8d.execute-api.ap-northeast-1.amazonaws.com/dev/iksm_session"
      const header = {
        "Content-Type": "application/json",
      }
      const response = fetch(url, {
        method: "POST",
        headers: header,
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(payload => {
        const response = JSON.parse(JSON.stringify(payload))
        console.log(payload)
        window.alert(response.iksm_session)
      })
    },
  },
  data() {
    return {
      summary: null,
      authorize_url: null
    }
  },
  mounted() {
    const summary = fetch("/summary/card.json")
    .then(r => r.json())
    .then(json => {
      this.summary = JSON.parse(JSON.stringify(json))
      console.log(summary)
    })
    const authorize = fetch("https://a9o2idgf8d.execute-api.ap-northeast-1.amazonaws.com/dev/authorize")
    .then(r => r.json())
    .then(json => {
      this.authorize_url = JSON.parse(JSON.stringify(json)).authorize_url
      console.log(this.authorize_url)
    })
  }
}
</script>

<template>
  <h1>Salmon Stats</h1>
  <div id="player-summary-overview" v-if="this.summary != null">
    <h2 class="power_eggs">Power Eggs {{ this.summary.ikura_total }}</h2>
    <h2 class="golden_eggs">Golden Eggs {{ this.summary.golden_ikura_total }}</h2>
  </div>
  <div id="authorize">
    <button @click="authorize()">Authorize</button>
    <button @click="input_code()">Input Address</button>
  </div>
</template>

<style scoped>
.power_eggs {
  color: red;
}

.golden_eggs {
  color: yellow;
}
</style>
