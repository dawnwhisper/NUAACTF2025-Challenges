#!/bin/bash

key=$1
k3y=()

if ! [[ "$key" =~ ^[0-9A-Za-z_{}]{42}$ ]]; then echo 🚫; exit 0; fi
function 🔢() { echo $(printf "%d" "'$1"); }
function 💣() {
    lock=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
    echo -n $lock | base64 -d > /tmp/💣;chmod +x /tmp/💣;
    key=$(echo -n $key | /tmp/💣 $key | base64)
    rm /tmp/💣
}
function ⛓️() {
    k3y=(${k3y[@]} $*)
}
function 🔒() {
    grep -o . <<< "$key" | while read -r k; do
        if ! [[ $(( $(🔢 "${k3y[-1]}") - $(🔢 "${k3y[0]}") )) == $(🔢 "$k") ]]; then
            return 1
        fi
        k3y=("${k3y[@]:1:$((${#k3y[@]}-2))}")
    done;
    return $?
}
function 🔐() {
    if [ $? == 0 ]; then echo 🔓; else echo 🔒; fi
}

⛓️ 🐏 🐠 🐠 🐃 🐦 🐇 🐁 \
🐞 🐅 🐓 🐈 🐌 🐂 🐄 🐄 
⛓️ 🐳 🐑 🐃 🐎 🐉 🐱 🐩 
⛓️ 🐅 🐟 🐕 🐀 🐄 🐄 🐄 \
🐍 🐏 🐅 🐈 🐗 🐋 🐏 🐋 \
🐞 🐙 🐉 🐆 🐘 🐶 🐁 🐊 \
🐊 🐢 🐓 🐘 🐐 🐭 🐘 🐇 
⛓️ 🐗 🐘 🐈 👾 👉 👏 👽 \
👾 👽 👳 👭 👬 👨 👴 👠 
💣 🐈 🐗 🐋 🐈 👾 👉 👏 \
⛓️ 👾 👽 👳 👭 👬 👨 👴
⛓️ 👰 👨 👌 👾 👻 👰 👫 \
👷 👾 👤 👬 👌 👧 👛 👤 \
👵 👷 👭 👋 👙 👲 👭 👽 
⛓️ 👡 👌 👻 👜 👳 👸 👽
⛓️ 👻 👔 👹 👺 👌 👼 👒 
⛓️ 👻 👟 👲 🐵 👫 👷 👖
🔒 👺 👌 👼 👒 🐉 🐆 🐘 \
⛓️ 🐁 🐊 🐊 🐢 🐓 🐘 🐐
🔐 🐋 🐈 👾 👻 👟 👲 🐵 
⛓️ 👫 👷 👖 🔒 🐉 🐆 🐘 \
🐁 🐊 🐊 🐢 🐓 🐘 🐐 🐭 

