<template>
    <div class="card">
        <div class="icon-box">
            <slot />
        </div>
    </div>
</template>

<style scoped>
.card {
  background-color: #111822;
  border-radius: 20px;
  padding: 22px 50px 22px 50px;
  max-width: 200px;
  text-align: center;
  transition: 
    opacity 0.3s,
    box-shadow 0.3s,
    transform 0.3s,
    background 0.3s,
    border-color 0.3s;
  cursor: pointer;
  border: 1px solid #374153;
  opacity: 0.8;
  box-shadow: 0 8px 22px 0 rgba(12, 41, 95, 0.712);
}
.card:hover {
  opacity: 1.0; 
  background-color: #323f5500; 
  border-color: #64748b69; 
  box-shadow: 0 4px 24px 0 rgba(60,80,120,0.20);
  transform: translateY(-4px) scale(1.03);
}

.icon-box {
  margin-left: auto;
  margin-right: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>