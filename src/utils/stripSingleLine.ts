export const stripSingleLine = (text: string): string => {
  const strippedText = text.trim();
  const singleLineText = strippedText.replace(/\n/g, " ");
  const words = singleLineText.split(/\s+/);
  const finalText = words.join(" ");

  return finalText;
};
