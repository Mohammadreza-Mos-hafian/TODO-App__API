/*--------------------------- Get Date --------------------------- */

const getYear = () => {
  const today = new Date();
  return today.getFullYear();
};

document.querySelector(".year").textContent = getYear();
