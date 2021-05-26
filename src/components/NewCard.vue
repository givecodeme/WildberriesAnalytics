<template>
  <div class="">
    <template #cell(stocks_qnt)="data">
      {{ data.value }} шт.
      <!-- <br />
          <span v-for="(stock, index) in data.item.stocks" :key="index">
            {{ stock.name }} - {{ stock.quantity }} шт.
            <br />
          </span> -->
    </template>

    <template #cell(orders_sum)="data">
      {{ data.value | format }} р.
      <p>{{ data.item.orders_qnt }} шт.</p>
    </template>

    <template #cell(delivery_sum)="data">
      {{ data.value | format }} р.
    </template>

    <template #cell(sales_sum)="data">
      {{ data.value | format }} р.
      <p>{{ data.item.sales_qnt }} шт.</p>
    </template>
    <template #cell(image)="data">
      <img :src="data.value" height="100" />
      <br />
      <a :href="data.item.wb_url" target="_blank" rel="noopener noreferrer">
        {{ data.item.nmid }}</a
      >
    </template>
  </div>
</template>

<script>
export default {
  props: ["data"],
};
</script>

<style>
</style>