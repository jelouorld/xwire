tree_with_contents() {
  for file in $(tree -fi --noreport); do
    if [[ -f $file ]] && [[ $file != *"mytree.sh" ]] && [[ $file != *"uv.lock" ]]; then
      echo -e "\n$file"
      sed 's/^/    /' "$file"
    fi
  done
}


tree_with_contents;
