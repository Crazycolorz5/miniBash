<script setup lang="ts">
import { ref, onUpdated, type Ref } from 'vue'

const stdout : Ref<string[]> = ref([]);
const stderr : Ref<string[]> = ref([]);
const pStdoutRef : Ref<null | HTMLElement> = ref(null);
const cdDir : Ref<string> = ref("");
const pFileInputRef : Ref<null | HTMLInputElement> = ref(null);

const server = "http://localhost:5000";

const debug = ref("This is debug text.");

async function updateUI(response : Response) {
    const data = await response.json();
    stdout.value = stdout.value.concat(data["stdout"].split('\n'));
    if(data["stderr"]) {
        stderr.value.push(data["stderr"]);
    }

}

async function get(command : string, api : string) {
    stdout.value.push("> " + command);
    const response = await fetch(server + api);
    await updateUI(response);
}

async function cd(d : string) {
    stdout.value.push("> cd " + d);
    const response = await fetch(server + "/cd", 
        { method:"POST",
          body: JSON.stringify({
            dir: d
          }),
          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
        }
    );
    updateUI(response);
}

async function cd_wrap() {
    const d = cdDir.value;
    cdDir.value = '';
    await cd(d);
}

function scrollStdOut() {
    const elem = pStdoutRef.value;
    if(elem !== null)
      elem.scrollTop = elem.scrollHeight;
}

onUpdated(scrollStdOut)

async function uploadFile() {
    const ref = pFileInputRef.value!;
    const files = ref.files;
    if(files !== null) {
      const fname = files[0].name;
      if(fname) {
          const formData = new FormData();
          formData.append('file', files[0]);
          stdout.value.push("> Uploading " + fname);
          ref.value = "";
          const response = await fetch(server + "/upload", 
              { method:"POST",
                body: formData
              }
          );
          await updateUI(response);
      } else { stderr.value.push("No file provided!"); }
    }
}

</script>

<template>
<div>
  <p> {{ debug }} </p>
  <div class="button-panel">
    <button class="button button_small" @click="get('ls', '/ls')">ls</button>
    <button class="button button_small" @click="get('pwd', '/pwd')">pwd</button>
    <button class="button button_small" @click="cd('..')">cd ..</button>
    <div style="width:25%; height:48px">
        <input v-model="cdDir" placeholder="cd directory" style="width:100%; height:40%; padding: 0px 0px"/>
        <button style="width:100%; height:60%; padding: 0px 0px" @click="cd_wrap()">cd</button>
    </div>
  </div>
  <div class="button-panel">
    <div style="width:50%; height:96px">
        <input type="file" ref="pFileInputRef" placeholder="Filename..."/>
        <button style="width:100%; height:60%; padding: 0px 0px" @click="uploadFile()">Upload File</button>
    </div>
  </div>
  <div class="terminal" ref="pStdoutRef">
    {{ stdout.join('\n') }}
  </div>
  <div style="color:red">
    {{ stderr.at(-1) }}
  </div>
</div>
</template>

<style scoped>

.button-panel {
    display: flex;
    justify-content: flex-start;
}
.button {
    padding: 16px 32px;
}
.button_thin {
    padding: 4px 32px;
}
.button_small {
    width: 25%;
}
.button_big {
    width: 50%;
}

.terminal {
    min-height: 300px;
    height: 300px;
    width: 90%;
    overflow: scroll;
    border: 3px solid #000000;
    padding: 3px;
    background-color: #202020;
    color: #F0F0F0;
    white-space: pre-wrap;
}

</style>
